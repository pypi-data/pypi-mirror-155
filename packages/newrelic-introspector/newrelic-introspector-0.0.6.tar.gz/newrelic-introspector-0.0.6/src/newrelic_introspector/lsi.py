from __future__ import print_function

import argparse
import json
import os
import re
import signal
import subprocess
import sys

try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping


ROOT_DIR = os.path.abspath(os.sep)
PROC_DIR = os.path.join(ROOT_DIR, "proc")
PYTHON_EXE_REGEX = re.compile(r"((python)|(pypy))(\d+(\.\d+(\.\d+)?)?)?")
NUMERIC_REGEX = re.compile(r"\s*\d+\s*")
DEFAULT_BIN_DIRS = [
    os.path.join(ROOT_DIR, "usr", "bin"),
    os.path.join(ROOT_DIR, "usr", "local", "bin"),
]
PY2 = sys.version[0] == "2"
DEFAULT_PYTHON_APP_NAME = "Python Application"
CONFIG_FILE_REPLACEMENTS = (
    ("# distributed_tracing.enabled", "distributed_tracing.enabled"),
    ("distributed_tracing.enabled = false", "distributed_tracing.enabled = true"),
    (
        "# application_logging.forwarding.enabled",
        "application_logging.forwarding.enabled",
    ),
    (
        "application_logging.forwarding.enabled = false",
        "application_logging.forwarding.enabled = true",
    ),
)


class RunMode:
    """Py2 compatible enum."""

    LIST = 1
    INTROSPECT = 2
    INSTALL = 3
    INSTRUMENT = 4


class ProcessTree(MutableMapping):
    def __init__(self):
        super(ProcessTree, self).__init__()

        # Initialize process dict
        self._storage = {
            int(pid): Process(pid)
            for pid in os.listdir(PROC_DIR)
            if NUMERIC_REGEX.match(pid) and int(pid) != os.getpid()
        }

        # Build links between parents and children
        for _, process in self._storage.items():
            if process.ppid:
                parent = self._storage[process.ppid]
                parent.children.add(process)
                process._parent = parent

    def __getitem__(self, key):
        return self._storage[key]

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)

    def __delitem__(self, key):
        return self._storage.__delitem__(key)

    def __setitem__(self, key, value):
        return self._storage.__setitem__(key, value)


class Process(object):
    def __init__(self, pid):
        super(Process, self).__init__()

        self.pid = int(pid)
        self.children = set()
        self._path = os.path.join(PROC_DIR, str(self.pid))
        self._ppid = None
        self._parent = None
        self._is_python = None
        self._command = None
        self._python_executable = None
        self._workdir = None
        self._environ = None
        self._stat = None

    def __int__(self):
        return int(self.pid)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    @property
    def ppid(self):
        if self._ppid is None:
            try:
                filename = os.path.join(self._path, "stat")
                with open(filename, "r") as file:
                    self._ppid = int(file.read().split(" ")[3])
            except FileNotFoundError:
                pass
            except PermissionError:
                print("Failed to read PPID for PID %d." % self.pid)

        return self._ppid

    @property
    def stat(self):
        if self._stat is None:
            self._stat = os.stat(self._path)
        return self._stat

    @property
    def uid(self):
        return self.stat.st_uid

    @property
    def gid(self):
        return self.stat.st_gid

    @property
    def contains_python(self):
        """Returns True if is_python for this process or any of its children is True."""
        if self.is_python:
            return True

        for child in self.children:
            if child.is_python:
                return True

        return False

    @property
    def is_python(self):
        """Returns True if this process directly contains python."""
        if self._is_python is None:
            self._is_python = False

            exe_basename = os.path.basename(self.command[0])
            if PYTHON_EXE_REGEX.match(exe_basename):
                self._is_python = True
                return True

            try:
                filename = os.path.join(self._path, "maps")
                with open(filename, "r") as file:
                    for line in file.readlines():
                        if "python" in line and "supervisord" not in line:
                            self._is_python = True
                            return True

            except FileNotFoundError:
                pass
            except PermissionError:
                print("Failed to read maps file on PID %d." % self.pid)

        return self._is_python

    @property
    def is_compatible_python_version(self):
        # Capture stdout of python version check
        output = subprocess.check_output([self.python_executable, "--version"])

        # If no output was captured
        if not output:
            print("Unable to check python verion for compatibility.")
            # Assuming compatibility for users' ease of use.
            return True

        # Convert stdout to a string, and parse out the Python version
        python_version = output.decode("utf-8").split(" ")[1].rstrip()
        is_py27 = python_version[0] == "2" and python_version[2] == "7"
        is_below_py36 = python_version[0] == "3" and int(python_version[2]) < 6
        if is_below_py36 and not is_py27:
            print(
                "Python "
                + python_version
                + " is not supported by the New Relic Python Agent. The agent supports Python 2.7 and 3.6+."
            )
            return False

        return True

    @property
    def is_process_manager(self):
        if "supervisord" in "".join(self.command):
            return True
        return False

    @property
    def command(self):
        """Parses and returns process command as a list."""
        if self._command is None:
            filename = os.path.join(self._path, "cmdline")
            with open(filename, "r") as file:
                self._command = file.read().strip().split("\0")
                self._command = list(filter(len, self._command))

        return self._command

    @property
    def python_executable(self):
        if self.is_python:
            if not self._python_executable:
                exe_basename = os.path.basename(self.command[0])
                if PYTHON_EXE_REGEX.match(exe_basename):
                    self._python_executable = self.command[0]
                else:
                    exe_dirname = os.path.dirname(self.command[0])
                    if exe_dirname and os.path.exists(exe_dirname):
                        python_exes = [
                            os.path.join(exe_dirname, x)
                            for x in os.listdir(exe_dirname)
                            if PYTHON_EXE_REGEX.fullmatch(x)
                        ]
                        self._python_executable = choice_input(
                            "Detected multiple possible python executables. "
                            "Please choose the executable you wish to use.",
                            python_exes,
                        )
                    else:  # No exe dir found
                        print(
                            "Python executable not found in base path of %s. Defaulting to %s"
                            % (str(self.command[0]), str(sys.executable))
                        )
                        self._python_executable = sys.executable

            return self._python_executable
        else:
            raise ValueError("Not a python process.")

    @property
    def newrelic_admin(self):
        executable = self.python_executable
        bin_dir = os.path.dirname(executable)
        admin_exe = os.path.join(bin_dir, "newrelic-admin")

        if not os.path.exists(admin_exe):
            # Check in default locations
            for bin_dir in DEFAULT_BIN_DIRS:
                fallback_admin_exe = os.path.join(bin_dir, "newrelic-admin")
                if os.path.exists(fallback_admin_exe):
                    return fallback_admin_exe

        # Return expected location if it exists, or if no fallbacks could be found.
        # Assumption will be that the command will be found after installation,
        # and will be picked up and run properly then.
        return admin_exe

    @property
    def workdir(self):
        if self._workdir is None:
            path = os.path.join(self._path, "cwd")
            self._workdir = os.path.realpath(path)

        return self._workdir

    @property
    def is_instrumentable(self):
        return (
            self.exists
            and self.is_base_python_process
            and self.is_compatible_python_version
        )

    @property
    def exists(self):
        # Proc directory exists, and command is non-empty
        return os.path.exists(self._path) and self.command

    @property
    def is_base_python_process(self):
        """Returns True if this process has no parent."""
        if self.is_process_manager:
            return False
        if not self.is_python:
            return False
        elif not self.ppid:
            return True
        elif not self._parent.is_python:
            return True

        return False

    @property
    def environ(self):
        """Parses and returns process environ as a dict."""
        if self._environ is None:
            filename = os.path.join(self._path, "environ")
            with open(filename, "r") as file:
                environ_list = file.read().strip().split("\0")
                environ_list = list(filter(len, environ_list))
                self._environ = dict(s.split("=", 1) for s in environ_list)

        return self._environ

    def rewrite_install_command(self):
        return (self.python_executable, "-m", "pip", "install", "newrelic")

    def rewrite_install_check_command(self):
        return (self.python_executable, "-m", "pip", "show", "newrelic")

    def rewrite_process_command(self):
        admin_command = [self.newrelic_admin, "run-program"]
        admin_command.extend(self.command)

        return tuple(admin_command)

    def get_app_name(self, args):
        if args.yes:
            return DEFAULT_PYTHON_APP_NAME

        print("\nOriginal process run with:\n", self.command)
        app_name = get_input("Enter an application name: ").strip()
        if app_name:
            return app_name
        else:
            print(
                "\nPlease enter an application name that is at least one character long."
            )
            return self.get_app_name(args)

    def generate_newrelic_config(self, args, ini_path):
        if (
            not os.path.exists(ini_path)
            or args.yes
            or yes_no_input(
                "\nnewrelic.ini file detected at %s. Would you like to overwrite it?"
                % str(ini_path)
            )
        ):
            app_name = args.appName or self.get_app_name(args)
            subprocess.call(
                [self.newrelic_admin, "generate-config", args.licenseKey, str(ini_path)]
            )
            with open(ini_path, "r+") as file:
                file_text = file.read()
                file.seek(0)
                file.truncate()

                for replace, replace_with in CONFIG_FILE_REPLACEMENTS:
                    file_text = file_text.replace(replace, replace_with)

                if args.region.upper() == "STAGING":
                    app_name += "\n\nhost = staging-collector.newrelic.com"

                file_text = file_text.replace(DEFAULT_PYTHON_APP_NAME, app_name)

                file.write(file_text)

    def install(self, args):
        install_command = self.rewrite_install_command()

        # Install New Relic
        sys.exit(subprocess.call(install_command))

    def instrument(self, args):
        check_command = self.rewrite_install_check_command()
        if subprocess.call(check_command):
            sys.exit("newrelic not installed.  run the --install command first")

        try:
            process_command = self.rewrite_process_command()
            if not process_command:
                raise ValueError("Failed to rewrite process command.")

            # Accept -y flag or prompt user for choice.
            yes = args.yes or yes_no_input(
                "\n%s\nAccept above command and restart process?"
                % " ".join(process_command)
            )
            if not yes:
                print("\nContinuing introspection without restarting process...")
                return False  # Exit if not accepted.

            # Detect existing config file
            if "NEW_RELIC_CONFIG_FILE" not in self.environ:
                # Set newrelic config file location in environment
                ini_path = os.path.join(self.workdir, "newrelic.ini")
                self.environ["NEW_RELIC_CONFIG_FILE"] = ini_path
            else:
                # Use existing newrelic config file location
                ini_path = self.environ["NEW_RELIC_CONFIG_FILE"]

            # Attempt to regenerate config file
            self.generate_newrelic_config(args, ini_path)

            # Kill original process
            os.kill(self.pid, signal.SIGTERM)

            # Start process with modified command
            print(
                "Using command: %s\nRestarting process..." % " ".join(process_command)
            )

            subprocess.Popen(process_command, env=self.environ, cwd=self.workdir)

        except Exception:
            print("\nFailed to instrument process.")

        return True


def list_instrumentable_pids(args):
    process_tree = ProcessTree()
    pids = [pid for pid, process in process_tree.items() if process.is_instrumentable]

    print(json.dumps(pids))


def introspect_pid(args):
    process_tree = ProcessTree()
    success = False

    process = process_tree.get(int(args.pid))
    if process.is_instrumentable:
        info = {
            "pid": args.pid,
            "uid": process.uid,
            "gid": process.gid,
            "ppid": process.ppid,
            "is_python": process.is_python,
            "contains_python": process.contains_python,
            "python_executable": process.python_executable,
            "cmd": " ".join(process.command),
        }

        success = True

    if not success:
        print("PID %d is not an introspectable python process." % args.pid)
        sys.exit(1)

    print(json.dumps(info))


def install_pid(args):
    success = False
    process_tree = ProcessTree()

    process = process_tree.get(int(args.pid))
    if process is not None and process.is_instrumentable:
        success = process.install(args)

    if not success:
        print("\nnewrelic agent could not be installed for PID %d." % process.pid)


def instrument_pid(args):
    success = False
    process_tree = ProcessTree()

    process = process_tree.get(int(args.pid))
    if process is not None and process.is_instrumentable:
        success = process.instrument(args)

    if not success:
        print("\nPID %d was not restarted or instrumented." % process.pid)


def yes_no_input(question):
    """Returns True if user responds with 'y'."""

    # Build prompt
    prompt = "%s [y/n]: " % question

    # Receive input from user
    try:
        response = str(get_input(prompt)).strip().lower()
    except Exception:
        response = None

    # Parse user input
    if response == "y":
        return True
    elif response == "n":
        return False
    else:
        print("Invalid response, expected [y/n]. Please try again.")
        # Recurse until answered
        return yes_no_input(question)


def choice_input(question, choices):
    """Returns user choice from iterable."""

    # Validate a choice must actually be made
    if not choices:
        return None
    elif len(choices) == 1:
        return choices[0]

    # Build prompt
    choice_strs = ["[%d]: %s" % (i, str(c)) for i, c in enumerate(choices)]
    choice_strs.insert(0, question)
    choice_strs.append("Choose a number: ")
    prompt = "\n".join(choice_strs)

    # Receive input from user
    try:
        response = int(get_input(prompt).strip().lower())
    except Exception:
        response = None

    # Parse user input
    if response is not None and response >= 0 and response < len(choices):
        return choices[response]
    else:
        print(
            "Invalid response, expected a number between 0-%d. Please try again."
            % (len(choices) - 1)
        )
        # Recurse until answered
        return choice_input(question, choices)


def get_input(prompt):
    """Compatibility function for Python 2/3. Gets user input based on prompt."""
    if PY2:
        return raw_input(prompt)  # pylint: disable=E0602 # noqa: F821
    else:
        return input(prompt)


def require_arg_defined(arg, args):
    if getattr(args, arg) is None:
        sys.stderr.write("--%s argument is required\n" % arg)
        sys.exit(1)


def require_pid(args):
    require_arg_defined("pid", args)
    try:
        pid = int(args.pid)
    except ValueError:
        sys.stderr.write("--pid must be an integer, got %s\n" % str(args.pid))
        sys.exit(1)

    if not Process(pid).exists:
        sys.stderr.write("--process with id %d does not exist\n" % pid)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--list",
        help="list the instrumentable PIDs",
        dest="mode",
        action="store_const",
        const=RunMode.LIST,
    )
    group.add_argument(
        "--introspect",
        help="introspect an instrumentable PID",
        dest="mode",
        action="store_const",
        const=RunMode.INTROSPECT,
    )
    group.add_argument(
        "--install",
        help="install the newrelic agent for a PID",
        dest="mode",
        action="store_const",
        const=RunMode.INSTALL,
    )
    group.add_argument(
        "--instrument",
        help="instrument an instrumentable PID",
        dest="mode",
        action="store_const",
        const=RunMode.INSTRUMENT,
    )

    parser.set_defaults(yes=False)
    parser.add_argument(
        "-y",
        "--yes",
        help="accept all prompts automatically",
        dest="yes",
        action="store_true",
    )

    parser.add_argument(
        "-r",
        "--region",
        choices=["US", "EU", "STAGING"],
        type=str.upper,
        help="the region to report into",
        default=os.environ.get("NEW_RELIC_REGION", "US"),
        dest="region",
    )

    parser.add_argument(
        "-k",
        "--licenseKey",
        help="the license key to use when reporting data",
        default=os.environ.get("NEW_RELIC_LICENSE_KEY"),
        dest="licenseKey",
    )

    parser.add_argument(
        "--pid",
        help="the process ID to introspect or instrument",
        dest="pid",
    )

    parser.add_argument(
        "-n",
        "--appName",
        help="the app name to use when reporting data",
        dest="appName",
    )

    args = parser.parse_args()

    if args.mode == RunMode.LIST:
        list_instrumentable_pids(args)
    elif args.mode == RunMode.INTROSPECT:
        require_pid(args)
        introspect_pid(args)
    elif args.mode == RunMode.INSTALL:
        require_pid(args)
        install_pid(args)
    elif args.mode == RunMode.INSTRUMENT:
        require_pid(args)
        require_arg_defined("licenseKey", args)
        instrument_pid(args)


if __name__ == "__main__":
    main()
