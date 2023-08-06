# Qlik SDK

Qlik's Python SDK allows you to leverage the APIs of Qlik Cloud platform from the comfort of python.

---

- [qlik-sdk-python](#qlik-sdk-python)
  - [Install](#install)
  - [Getting started](#getting-started)
  - [Authentication options](#authentication-options)
    - [API keys](#api-keys)
  - [Changelog](#changelog)
  - [Contributing](#contributing)
    - [Bugs](#bugs)
    - [Features](#features)
    - [Developing](#developing)

---

## Install

```bash
python3 -m pip install --upgrade qlik-sdk
```

## Getting started

A good place to start is our [examples](./examples/). Take a look and learn how to authorize and use our REST and RPC clients to access the APIs. If you're in a real hurry, the essence of our examples is shown below.

```python
from qlik_sdk import Auth, AuthType, Config

api_key = "<MY_API_KEY>"
base_url = "<URL_TO_MY_TENANT>" # E.g. https://foo.qlikcloud.eu.com

auth = Auth(Config(host=base_url, auth_type=AuthType.APIKey, api_key=api_key))

# For REST calls: auth.rest
# For RPC calls: auth.rpc
```

## Authenticiation options

### API keys

An API key is a token representing a user in your tenant. Anyone may interact with the platform programmatically using the API key. The token contains the user context, respecting the access control privileges the user has in your tenant. More info can be found on [Qlik Dev Portal](https://qlik.dev/basics/authentication-options#api-keys).

For a step-by-step guide on how to get an API key for your tenant, check this [tutorial](https://qlik.dev/tutorials/generate-your-first-api-key).

## Changelog

Detailed changes for each release are documented in the [release notes](./CHANGELOG.md).

## Contributing

Please make sure to read and follow our [Code of conduct](https://github.com/qlik-oss/open-source/blob/master/CODE_OF_CONDUCT.md)

### Bugs

Bugs can be reported by adding issues in the repository. Please use the Bug Report template.

### Features

Features can also be reported by adding issues in the repository. Please use the Feature Request template.

### Developing

```bash
# install dependencies
make install-requirements-dev

# lint
make lint

# run tests
make test
make test-unit
make test-e2e
```

#### Install pre-commit-hook

```bash
make install-pre-commit
```

Run `make install-debug` to debug the local code through the examples.

### Release

- Update version in `src/qlik_sdk/_version.py` and push to main
- Update tag `git tag <version>` and push tag to main `git push --tags`
- Should trigger gha: "Publish PyPi"
