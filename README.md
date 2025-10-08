---
title: Multi-agent-system
emoji: 🐳
colorFrom: purple
colorTo: gray
sdk: docker
app_port: 7860
---

# Multi-Agent AI System

A modular, full-stack AI orchestration platform for document analysis, web search, and academic research. Built for internship and research demonstration purposes, it features intelligent query routing and a transparent multi-agent workflow.

**🚀 Live Demo:** [View on Hugging Face Spaces](https://huggingface.co/spaces/Fox8081/Multi-Agent-AI-System)

---

## 🧠 System Architecture

The platform employs a **multi-agent architecture** with a central **Controller Agent** (Groq LLM-powered). User queries are dynamically routed to one or more specialized agents based on context:

- **PDF RAG Agent:**  
  Handles document Q&A using Retrieval-Augmented Generation and FAISS vector search on user-uploaded PDFs.

- **Web Search Agent:**  
  Provides real-time internet search results for current events and general knowledge.

- **ArXiv Agent:**  
  Fetches, analyzes, and summarizes academic papers from the ArXiv repository.

**Tech Stack:**  
- Backend: **Flask**  
- Frontend: Custom UI: **HTML, CSS, JS**
- LLM API: **Groq**  
- Containerization: **Docker**  
- Deployment: **Hugging Face Spaces**

---

## ✨ Features

- **Intelligent Agent Routing:**  
  Controller chooses the best agent(s) for each query.

- **Document Analysis:**  
  Upload PDFs and ask context-aware questions.

- **Web & Academic Search:**  
  Integrated web search and scientific paper summarization.

- **Transparent Decisions:**  
  UI displays which agents handled each query and controller's reasoning.

- **Traceability & Logging:**  
  All agent interactions and routing decisions are logged.  
  Access logs via the `/logs` endpoint.

- **Extensible Design:**  
  Modular structure for easy addition of new agents or features.

---

## 🛠️ Local Development & Setup

Clone and run locally in minutes:

### 1. Clone the repository
```bash
git clone https://github.com/Fox8081/Multi-agent-system.git
cd Multi-agent-system
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# On Unix/macOS:
source venv/bin/activate
# On Windows:
.\venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 4. Add environment variables
- Create a file named `.env` in the root directory.
- Add your Groq API Key (never commit this file!):
  ```
  GROQ_API_KEY="your-secret-key-here"
  ```

### 5. Run the application
```bash
python -m backend.main
```

- The app will be available at: [http://127.0.0.1:5001](http://127.0.0.1:5001)

---

## 🚦 Deployment

The app is containerized for reproducible deployment.
- See [Dockerfile](./Dockerfile) for build instructions.
- For cloud deployment, use [Hugging Face Spaces](https://huggingface.co/spaces/Fox8081/Multi-Agent-AI-System) or Render.

---

## 🗂️ Repo Structure

```
agents/           # Specialized agent classes and logic
backend/          # Flask backend, controller and routing
frontend/         # UI code and static assets
tests/            # Unit and integration tests
sample_pdfs/      # Example PDFs for demo (generated from NebulaByte dialogs)
logs/             # Controller and agent interaction logs
requirements.txt  # Python dependencies
Dockerfile        # Containerization config
README.md         # This file
REPORT.pdf        # System report, architecture, and analysis
.env              # Your API keys (never commit!)
```

---

## 📄 Documentation & References

- See [REPORT.pdf](./REPORT.pdf) for full architecture, controller logic, privacy/safety handling, and system limitations.
- The [sample_pdfs/](./sample_pdfs/) folder contains 5 curated demo PDFs (generated from NebulaByte dialogs) for RAG evaluation.

---

## 🧪 Testing

Run all tests:
```bash
pytest tests/
```

---

## 🔒 Security & Privacy

- **API keys:** Always store secrets in `.env` (add `.env` to `.gitignore`).
- **Logs:** Sensitive information is excluded from public logs.
- **User data:** Uploaded PDFs are processed in-memory and not stored persistently.

---

## 🤝 Contributing

Pull requests are welcome!  
Please see [CONTRIBUTING.md](./CONTRIBUTING.md) if available, or open an issue for questions.

---


