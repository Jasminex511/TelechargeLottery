#!/bin/bash

cd "$(dirname "$0")" || exit 1  # Exit the script with a non-zero status if `cd` fails

source .venv/bin/activate
python telecharge.py