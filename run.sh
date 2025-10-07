#!/bin/bash

# Set the cache directory to a writable location inside our app folder
export TRANSFORMERS_CACHE='/app/cache'

# Run the gunicorn server
gunicorn --bind 0.0.0.0:7860 backend.main:app