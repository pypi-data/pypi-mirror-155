import os

from flask import Flask

app = Flask(__name__)
application = app


@app.route("/")
def hello():
    return "Hello World!\n"


@app.route("/env_test")
def env_test():
    if not os.environ.get("TEST_ENV_VAR", None):
        raise RuntimeError()
    return "TEST_ENV_VAR exists.\n%s\n" % str(os.environ)


if __name__ == "__main__":
    app.run(port=8000)
