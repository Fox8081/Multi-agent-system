import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

# I'm creating a class for the RAG agent to hold the model and the vector stores.
# This is better than using global variables because it keeps everything organized.
class RAGAgent:
    def __init__(self):
        # Using 'all-MiniLM-L6-v2'. It's a great model that's fast and effective,
        # perfect for running on a local machine without a powerful GPU.
        print("-> Initializing RAG Agent: Loading embedding model...")
        os.environ["HF_HOME"] = "/tmp"
        os.environ["TRANSFORMERS_CACHE"] = "/tmp"
        os.environ["SENTENCE_TRANSFORMERS_HOME"] = "/tmp"
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        # This dictionary will store the FAISS indexes in memory.
        # The key will be the file_id, so we can handle multiple PDF uploads.
        self.vector_stores = {}
        self.text_chunks = {}
        print("-> RAG Agent initialized.")

    def process_pdf(self, file_path, file_id):
        print(f"-> Processing PDF for file_id: {file_id}")
        # 1. Load text from the PDF using PyMuPDF
        doc = fitz.open(file_path)
        text = "".join(page.get_text() for page in doc)
        if not text:
            print(f"Warning: No text found in PDF: {file_id}")
            return "Could not extract text from the PDF."

        # 2. Chunk the text.
        # LLMs have a context limit, so we need to split the text into smaller pieces.
        # RecursiveCharacterTextSplitter is good at keeping related text together.
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_text(text)
        self.text_chunks[file_id] = chunks

        # 3. Embed the chunks and store in FAISS.
        # FAISS is a library for super-fast similarity search.
        print(f"-> Creating embeddings for {len(chunks)} chunks...")
        embeddings = self.model.encode(chunks)
        
        # FAISS requires a numpy array of float32.
        embeddings = np.array(embeddings).astype('float32')
        
        # IndexFlatL2 is a basic but effective index for our purpose.
        # It performs a brute-force search, which is fine for the number of chunks
        # we'll have from a single PDF.
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        self.vector_stores[file_id] = index
        print(f"-> PDF processed and indexed for file_id: {file_id}")
        return "PDF processed successfully."

    def query_pdf(self, query, file_id, k=3):
        print(f"-> Querying PDF for file_id: {file_id}")
        if file_id not in self.vector_stores:
            return "Error: This PDF has not been processed yet. Please upload it again."
        
        # 4. Retrieve relevant chunks.
        # First, we embed the user's query into a vector.
        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype('float32')
        
        # Then, we search the FAISS index for the 'k' most similar chunk vectors.
        index = self.vector_stores[file_id]
        distances, indices = index.search(query_embedding, k)
        
        # We retrieve the actual text chunks using the indices found by FAISS.
        retrieved_chunks = [self.text_chunks[file_id][i] for i in indices[0]]
        
        context = "\n\n---\n\n".join(retrieved_chunks)
        return context