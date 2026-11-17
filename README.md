# 📄 Chat with Your PDF

A RAG (Retrieval-Augmented Generation) app: upload any PDF, ask questions in plain English, and get answers with page citations.

## How it works
1. Extract text from the PDF (pypdf)
2. Split into overlapping chunks
3. Convert chunks to embeddings (sentence-transformers, all-MiniLM-L6-v2)
4. Store and search with FAISS
5. Send the top matching chunks to an LLM (Groq) to write the answer
6. Show the answer with the source pages

## Tech stack
Python, Streamlit, FAISS, sentence-transformers, Groq API

## Run locally
1. Clone the repo and create a virtual environment
2. `pip install -r requirements.txt`
3. Create a `.env` file with `GROQ_API_KEY=your_key`
4. `streamlit run src/app.py`

## What I learned
- Built a local RAG pipeline from scratch, handling Python environment setup and library compatibilities.
- Integrated vector embeddings with semantic search and connected a high-speed LLM via Groq to provide accurate, cited answers.