from flask import Flask, request, jsonify
from config import GROQ_API_KEY

# Initializing the Flask application. Flask is a lightweight framework,
# which is perfect for this project because it's simple and lets me focus on the agent logic.
app = Flask(__name__)

# It's good practice to check if the API key was loaded correctly on startup.
# This simple check will stop the app if the .env file is missing or incorrect.
if not GROQ_API_KEY:
    raise ValueError("ERROR: GROQ_API_KEY not found. Make sure you have a .env file with the key.")
else:
    print("-> GROQ API Key loaded successfully.")


@app.route('/ask', methods=['POST'])
def ask():
    # This is a placeholder for now. It just confirms that the endpoint
    # receives the query from the frontend.
    data = request.get_json()
    query = data.get('query')
    print(f"-> Received query: {query}")
    return jsonify({
        "answer": f"Backend received your query: '{query}'. The real logic is coming soon!",
        "agents_used": ["Placeholder Agent"]
    })

# TODO: Implement the actual file saving and processing logic later.
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    print(f"-> Received file: {file.filename}")
    # For now, just confirming we got the file.
    return jsonify({"message": f"File '{file.filename}' received. Processing to be implemented.", "file_id": "temp_file_123"})


# This endpoint will eventually show our trace logs.
@app.route('/logs', methods=['GET'])
def get_logs():
    # Placeholder log data for now.
    return jsonify([{"log": "System is running. Logging to be implemented."}])

# This block allows us to run the server directly from the command line
# using 'python backend/main.py'. The debug=True flag is super helpful
# for development as it automatically reloads the server when we save changes.
if __name__ == '__main__':
    print("-> Starting Flask server in debug mode...")
    app.run(debug=True, port=5001)