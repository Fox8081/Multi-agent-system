import json
from backend.config import GROQ_API_KEY
from groq import Groq

# I'm setting up the Groq client here. It will use the API key we loaded in the config.
client = Groq(api_key=GROQ_API_KEY)

def route_query(query: str, file_id_present: bool):
    """
    Decides which tool to use based on the user's query.
    This is a simple but effective hybrid approach: rule-based for common cases,
    and LLM-based for everything else.
    """
    print(f"-> Routing query: '{query}'")

    # 1. Rule-based routing for simple, obvious cases.
    # This is fast and cheap, a good first check.
    query_lower = query.lower()
    if file_id_present and ("this document" in query_lower or "summarize" in query_lower):
        print("-> Decision (Rule-based): PDF-RAG")
        return {"tool": "PDF-RAG", "rationale": "Query refers to the uploaded document, so the PDF-RAG agent was chosen."}
    if "arxiv" in query_lower or "paper" in query_lower or "research" in query_lower:
        print("-> Decision (Rule-based): ArxivSearch")
        return {"tool": "ArxivSearch", "rationale": "Query contains keywords like 'arxiv' or 'paper', suggesting an academic search."}
    if "latest news" in query_lower or "current events" in query_lower:
        print("-> Decision (Rule-based): WebSearch")
        return {"tool": "WebSearch", "rationale": "Query asks for current news, so the Web Search agent is appropriate."}

    # 2. LLM-based routing for more complex or ambiguous queries.
    print("-> Decision (LLM-based): Consulting Groq for routing...")
    system_prompt = """
    You are an expert routing agent. Your task is to analyze a user query and decide the best tool to use.
    You have three tools available:
    1. WebSearch: For real-time information, news, current events, or general knowledge questions.
    2. ArxivSearch: For scientific papers, research, technical topics, and academic queries.
    3. PDF-RAG: Use ONLY if the user explicitly refers to an uploaded document. A file_id will be provided.

    Respond in a simple JSON format like: {"tool": "YourChoice", "rationale": "Your reasoning."}
    Your choice must be one of: "WebSearch", "ArxivSearch", or "PDF-RAG".
    """
    prompt = f"User Query: '{query}'\nFile ID provided: {file_id_present}"

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0,
            response_format={"type": "json_object"},
        )
        decision_json = chat_completion.choices[0].message.content
        decision = json.loads(decision_json)
        print(f"-> Groq Decision: {decision}")
        return decision
    except Exception as e:
        print(f"Error during LLM routing: {e}")
        # Fallback to web search if the LLM fails for any reason.
        return {"tool": "WebSearch", "rationale": "LLM routing failed, falling back to a general web search."}


def synthesize_answer(query, context, client):
    """
    Synthesizes a final, Markdown-formatted answer from multiple context sources.
    """
    print("-> Synthesizing final answer...")

    if not context.strip():
        return "I couldn't find enough information to answer that question."

    messages = [
        {"role": "system", "content": (
            "You are a helpful and friendly AI assistant. "
            "Using the provided context, write a clear and complete Markdown-formatted answer. "
            "Use bold text (**like this**) for key points."
        )},
        {"role": "user", "content": f"Context:\n{context}\n\nUser Query: {query}"}
    ]

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[Error] synthesize_answer: {type(e).__name__} - {e}")
        return "There was an error generating the final answer."
