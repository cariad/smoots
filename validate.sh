#!/bin/bash

set -euo pipefail

find . -name "*.sh" -exec shellcheck -o all --severity style -x {} +

yamllint --strict .

if [[ "${CI:=}" == "true" ]]; then
  black . --check --diff --line-length 79
else
  black . --line-length 79
fi

if [[ "${CI:=}" == "true" ]]; then
  isort . --check-only --diff
else
  isort .
fi

flake8 .

mypy smoots
mypy tests

pytest -vv
