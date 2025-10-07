#!/bin/bash

# Set the cache directory to a writable location
export TRANSFORMERS_CACHE='/app/cache'

# Clear out any old model cache to save space
rm -rf $TRANSFORMERS_CACHE

# Run the gunicorn server
python -m gunicorn --bind 0.0.0.0:7860 backend.main:app