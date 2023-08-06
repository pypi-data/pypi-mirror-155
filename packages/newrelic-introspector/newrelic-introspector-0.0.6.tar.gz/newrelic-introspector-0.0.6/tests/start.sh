#!/bin/bash
CONDA_PREFIX=$(conda info --base)
set -e

export TEST_ENV_VAR="12=3"

if [[ -e "/venv" ]]; then
	source /venv/bin/activate
elif [[ -n "$CONDA_PREFIX" ]]; then
	source $CONDA_PREFIX/etc/profile.d/conda.sh
	conda activate app_env
fi

gunicorn main:app -w3 -b 0.0.0.0:8000
