# Python Sonarqube Client

This library provide a programmatic interface to interact with SonarQube.
It exposes both a client class and a CLI.

* Fore more information, checkout [sonar-client documentation](https://sylvanld.gitlab.io/open-source/python-sonar-client)

## Installation

```bash
pip install sonar-client
```

## Example Usage

**Using python interface**

```python
from sonar_client import SonarClient

sonar_token = "fake-token"
sonar = SonarClient(sonar_token, sonar_url="https://sonarcloud.io")
projects = sonar.search_project(organization="myorg")
```

**Using CLI interface**

You can discover available CLI commands by using `--help` options.

```bash
$ sonar-cli --help
Usage: sonar-cli [OPTIONS] COMMAND [ARGS]...

  SonarQube CLI

Options:
  --token TEXT  Sonar access token
  --help        Show this message and exit.

Commands:
  project  Sonar project management
```

```bash
$ sonar-cli project create --help
Usage: sonar-cli project create [OPTIONS]

  Create sonarqube project

Options:
  --org TEXT    Sonar organization  [required]
  --key TEXT    Sonar project key  [required]
  --title TEXT  Sonar project title  [required]
  --help        Show this message and exit.
```
