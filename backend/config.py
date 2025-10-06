import os
from dotenv import load_dotenv

# I'm using the python-dotenv library to load our API key from a .env file.
# This is a good security practice to keep secrets out of the main code.
print("-> Loading environment variables...")
load_dotenv()

# Get the Groq API key from the environment.
# os.getenv() will return None if the key isn't found, which is helpful for debugging.
GROQ_API_KEY = os.getenv("GROQ_API_KEY")