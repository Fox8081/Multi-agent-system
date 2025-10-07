#!/bin/bash

# Set the cache directory to a writable location
export TRANSFORMERS_CACHE='/app/cache'

# Add the app directory to Python's path so it can find the 'backend' module
export PYTHONPATH=/app

# Run the gunicorn server
gunicorn --bind 0.0.0.0:7860 backend.main:app