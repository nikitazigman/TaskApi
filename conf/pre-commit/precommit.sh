#!/bin/bash

echo source venv

source venv/bin/activate


echo run black
black --config conf/linters_and_fixers/pyproject.toml service/

echo run isort
isort service/

echo run flake8
flake8 --config=conf/linters_and_fixers/.flake8 service
