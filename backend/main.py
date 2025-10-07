import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from backend.config import GROQ_API_KEY
from backend.logging_utils import app_logger
# Importing our agent functions and classes
from agents.controller import route_query, synthesize_answer, client
from agents.pdf_rag import RAGAgent
from agents.web_search import search_web
from agents.arxiv import search_arxiv

# --- Initialization ---
# I'm initializing the Flask app and the RAG agent here, at the start.
app = Flask(__name__, static_folder='../frontend', static_url_path='')
rag_agent = RAGAgent()

# A simple check to make sure the API key is loaded.
if not GROQ_API_KEY:
    raise ValueError("ERROR: GROQ_API_KEY not found. Make sure you have a .env file with the key.")
else:
    app_logger.info("GROQ API Key loaded successfully.")

# --- Frontend Route ---
# This will serve our main HTML file for the UI.
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# --- API Endpoints ---
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # It's a good practice to save uploaded files to a temporary directory.
    # I'm creating a 'temp_uploads' folder if it doesn't exist.
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Using uuid to create a unique filename to avoid conflicts.
    file_id = str(uuid.uuid4())
    file_path = os.path.join(temp_dir, f"{file_id}.pdf")
    file.save(file_path)
    
    # Now, process the saved PDF with our RAG agent.
    rag_agent.process_pdf(file_path, file_id)
    
    app_logger.info(f"File uploaded and processed...")
    return jsonify({"message": f"File '{file.filename}' uploaded successfully.", "file_id": file_id})


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('query')
    file_id = data.get('file_id') # This can be None if no file was uploaded

    if not query:
        return jsonify({"error": "Query is required."}), 400

    # 1. Controller decides which tool to use.
    file_id_present = file_id is not None
    decision = route_query(query, file_id_present)
    tool_to_use = decision.get("tool")
    rationale = decision.get("rationale")
    
    context = ""
    # 2. Call the appropriate agent based on the controller's decision.
    if tool_to_use == "PDF-RAG":
        if not file_id:
            context = "Error: The controller decided to use the PDF, but no PDF was provided."
        else:
            context = rag_agent.query_pdf(query, file_id)
    elif tool_to_use == "ArxivSearch":
        context = search_arxiv(query)
    elif tool_to_use == "WebSearch":
        context = search_web(query)
    else:
        # A fallback just in case the LLM gives a weird response.
        context = search_web(query)
        rationale += " (Fallback to web search due to unexpected tool choice)."

    # 3. Synthesize the final answer using the context.
    final_answer = synthesize_answer(query, context, client)

    return jsonify({
        "answer": final_answer,
        "agents_used": [tool_to_use],
        "rationale": rationale
    })


# TODO: completed the task 
@app.route('/logs', methods=['GET'])
def get_logs():
    """
    This endpoint reads the trace.log file and returns its content.
    This fulfills the requirement to have an accessible log trace.
    """
    try:
        with open('trace.log', 'r') as f:
            logs = f.read()
        # Returning the log content as plain text for simplicity.
        return logs, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except FileNotFoundError:
        return "Log file not found.", 404


if __name__ == '__main__':
    app.run(debug=True, port=5001)