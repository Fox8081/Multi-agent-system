# I'm starting with a lean official Python image. This keeps the final container size smaller.
FROM python:3.11-slim

# Set the working directory inside the container to /app.
# This is where our project files will live.
WORKDIR /app

# Copy the requirements file first. This is a clever trick for Docker caching.
# If the requirements don't change, Docker can reuse this layer, making future builds faster.
COPY requirements.txt .

# Install all the Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the run script and make it executable
COPY run.sh .
RUN chmod +x run.sh

# Expose the port the app runs on
EXPOSE 7860

# Run the application using our new script
CMD ["./run.sh"]