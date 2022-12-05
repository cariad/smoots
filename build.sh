#!/bin/bash

set -euo pipefail

echo "${1:?}" > smoots/VERSION

rm -rf dist
python setup.py bdist_wheel
rm -rf build
