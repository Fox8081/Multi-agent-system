# I'm starting with a lean official Python image. This keeps the final container size smaller.
FROM python:3.10-slim

# Set the working directory inside the container to /app.
# This is where our project files will live.
WORKDIR /app

# Copy the requirements file first. This is a clever trick for Docker caching.
# If the requirements don't change, Docker can reuse this layer, making future builds faster.
COPY requirements.txt .

# Install all the Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Now, copy the rest of the project files into the /app directory in the container.
COPY . .

# Tell Docker that the container will listen on port 7860.
# Hugging Face Spaces uses this port by default for web apps.
EXPOSE 7860

# This is the command that will run when the container starts.
# It uses Gunicorn, a proper production server, to run our Flask app from main.py.
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "backend.main:app"]