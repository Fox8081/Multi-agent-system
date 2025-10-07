#!/bin/bash

# Set the cache directory to a writable location
export TRANSFORMERS_CACHE='/app/cache'

# Run gunicorn as a Python module to ensure paths are handled correctly
python -m gunicorn --bind 0.0.0.0:7860 backend.main:app