#!/bin/bash

# Create a writable cache directory if it doesn’t exist
mkdir -p /app/cache
chmod -R 777 /app/cache

# Use the new environment variable for Hugging Face model caching
export HF_HOME='/app/cache'

# Start the Flask app via Gunicorn
python -m gunicorn --chdir backend --bind 0.0.0.0:7860 main:app
