# Start from a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Make the run script executable
RUN chmod +x run.sh

# Expose the app port
EXPOSE 7860

RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

ENV HF_HOME=/tmp
ENV TRANSFORMERS_CACHE=/tmp
ENV SENTENCE_TRANSFORMERS_HOME=/tmp


# Run the app
CMD ["./run.sh"]
