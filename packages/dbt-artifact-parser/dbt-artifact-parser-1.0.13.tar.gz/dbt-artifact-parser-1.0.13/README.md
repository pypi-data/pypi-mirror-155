# dbt-artifact-parser

An open source project to parse dbt artifacts which can be later used for alerting purposes.

Supporting repository to setup the alerting service can be found [here](https://github.com/zoe/dbt-alerting-service)

## Setup

While it is not necessary, we advise using a virtual environment with Python >= 3.8 before contributing to this project.

1. Run `make init` to setup the necessary dependencies and commit hooks.

## Testing

Run `make test` to run all tests.

## Upload new version to PyPi

```
pip install twine
python setup.py sdist
twine upload dist/*
```

## Help

To see all the available commands for the repo, you can run `make help`
