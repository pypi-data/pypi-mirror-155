[![Community Project header](https://github.com/newrelic/opensource-website/raw/master/src/images/categories/Community_Project.png)](https://opensource.newrelic.com/oss-category/#community-project)

# newrelic-introspector-python

This is a CLI tool for discovering instrumentable Python applications on a system,
retrieving contextual information about them, and automating the install of the New Relic python agent.

## Getting Started

```
> python3 src/lsi.py --list
[12345]

> python3 src/lsi.js --introspect --pid 12345
{"pid": 12345, "uid": 1000, "gid": 1000, "ppid": 1, "is_python": true, "contains_python": true, "python_executable": "/usr/bin/python3", "cmd": "/usr/bin/python3 /home/ec2-user/app/main.py"}

> python3 src/lsi.py --install --pid 12345

> python3 src/lsi.py --instrument --pid 12345 --licenseKey $NEW_RELIC_LICENSE_KEY --appName "My Python Application"
...

```

## Instrumenting processes

The `instrument` command automates several installation steps:

1. Verifies that the [newrelic package](https://pypi.org/project/newrelic/) has been successfully installed.
2. Generates a newrelic.ini configuration file. If one already exists, an option will be provided to keep or overwrite it. 
3. Restarts the process using the [newrelic-admin script](https://docs.newrelic.com/docs/agents/python-agent/installation/python-agent-admin-script-advanced-usage/#run-program). 

Instrumentation will survive further restarts, but may be lost if the application is redeployed or any other actions are taken that revert the changes above.

## Support

New Relic hosts and moderates an online forum where customers can interact with New Relic employees as well as other customers to get help and share best practices. Like all official New Relic open source projects, there's a related Community topic in the New Relic Explorers Hub. You can find this project's topic/threads here:

<https://discuss.newrelic.com/tags/pythonagent>

## Contribute

We encourage your contributions to improve newrelic-introspector-python! Keep in mind that when you submit your pull request, you'll need to sign the CLA via the click-through using CLA-Assistant. You only have to sign the CLA one time per project.

If you have any questions, or to execute our corporate CLA (which is required if your contribution is on behalf of a company), drop us an email at opensource@newrelic.com.

**A note about vulnerabilities**

As noted in our [security policy](../../security/policy), New Relic is committed to the privacy and security of our customers and their data. We believe that providing coordinated disclosure by security researchers and engaging with the security community are important means to achieve our security goals.

If you believe you have found a security vulnerability in this project or any of New Relic's products or websites, we welcome and greatly appreciate you reporting it to New Relic through [HackerOne](https://hackerone.com/newrelic).

If you would like to contribute to this project, review [these guidelines](./CONTRIBUTING.md).

To [all contributors](https://github.com/newrelic/newrelic-introspector-python/graphs/contributors), we thank you!  Without your contribution, this project would not be what it is today.

## License

newrelic-introspector-python is licensed under the [Apache 2.0](http://apache.org/licenses/LICENSE-2.0.txt) License.
