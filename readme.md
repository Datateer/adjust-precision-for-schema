# Adjust Precision for Schema

Certain data sources, targets, and Python are incompatible regarding numeric precision. For example, PostgreSQL and MongoDB have higher precision than Python, leading to a decimal.DivisionImpossible error from jsonschema validators. You can see a more detailed explanation of this at https://cmsdk.com/python/decimal-invalidoperation-divisionimpossible-for-very-large-numbers.html

[target-postgres solves this](https://github.com/meltano/target-postgres/blob/8c792d87b8a28205e82deb607e84f45781fdb886/target_postgres/__init__.py#L36-L68) by walking the schema (even going into nested JSON) and adjusting the precision as needed.

This project encapsulates and improves that functionality in a standalone repository for use in any singer-io target that needs it.

## Prerequisites

- Python ^3.8
- Poetry

## Setup

- run `poetry install`
- run `poetry run pre-commit install`
