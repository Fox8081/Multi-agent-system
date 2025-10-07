#!/bin/bash

# Ensure writable cache directory (for HF / transformers / embeddings)
export TRANSFORMERS_CACHE='/app/cache'

# Start the Flask app via Gunicorn as a Python module
# --chdir backend → tells Gunicorn to look inside /app/backend
# main:app → loads the 'app' instance from main.py
python -m gunicorn --chdir backend --bind 0.0.0.0:7860 main:app
