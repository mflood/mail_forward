#!/bin/sh
source venv/bin/activate
pip install -e .
pytest -vv
