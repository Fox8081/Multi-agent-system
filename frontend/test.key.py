import os
from dotenv import load_dotenv
from groq import Groq

print("--- Starting API Key Test ---")

# 1. Load the .env file
load_dotenv()
print("Attempted to load .env file.")

# 2. Read the key from the environment
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("\nERROR: API key not found in environment variables.")
    print("Please check that your .env file is named correctly and is in the same directory as this script.")
else:
    print(f"API Key Found: ...{api_key[-4:]}") # Print the last 4 characters to confirm it's loaded

    # 3. Try to use the key to make a simple API call
    try:
        print("\nAttempting to connect to Groq...")
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": "Hello Groq"}],
            model="llama3-8b-8192",
        )
        print("SUCCESS: Connection to Groq API was successful!")
        print("Response:", chat_completion.choices[0].message.content)
    except Exception as e:
        print("\nERROR: Failed to connect to Groq API.")
        print(f"The error was: {e}")

print("\n--- Test Finished ---")