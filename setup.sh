#!/usr/bin/env bash

set -e

python -m venv .venv

source .venv/bin/activate

pip3 install -r requirements.txt
