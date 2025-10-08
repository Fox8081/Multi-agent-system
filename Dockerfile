# Set the working directory inside the container
FROM python:3.11-slim
WORKDIR /app

# Create writable directories for logs, cache, and uploads
RUN mkdir -p /app/logs && chmod -R 777 /app/logs
RUN mkdir -p /app/cache && chmod -R 777 /app/cache
RUN mkdir -p /app/temp_uploads && chmod -R 777 /app/temp_uploads

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the embedding model during build
# Set HF_HOME to /app/cache for build process
ENV HF_HOME=/app/cache
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy the rest of your application code
COPY . .

# Ensure environment variables are set for runtime as well
ENV HF_HOME=/app/cache
ENV TRANSFORMERS_CACHE=/app/cache
ENV SENTENCE_TRANSFORMERS_HOME=/app/cache

# Expose the port your Flask app runs on
EXPOSE 7860

# Command to run your application using gunicorn
# (You can also use a run.sh script for more complex startups)
CMD exec gunicorn --bind 0.0.0.0:7860 --workers 1 backend.main:app