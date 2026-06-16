# Bhagavad Gita AI Guide

A simple beginner-friendly Python RAG project that helps users ask life questions and receive guidance based on relevant Bhagavad Gita verses.

This project is intentionally small. It does not use a production-level architecture.

## Project Structure

```text
Bhagavad_Gita_AI/
├── app.py
├── rag.py
├── ingest.py
├── prompt.py
├── download_dataset.py
├── streamlit_app.py
├── .env
├── requirements.txt
├── README.md
├── data/
│   └── bhagavad_gita.json
└── chroma_db/
```

## File And Folder Purpose

### `app.py`

FastAPI backend. It receives a user question, searches relevant verses, builds a prompt, calls Gemini, and returns guidance.

### `rag.py`

Searches the local ChromaDB database for the most relevant Bhagavad Gita verses.

### `ingest.py`

Reads `data/bhagavad_gita.json`, creates embeddings, and stores them in ChromaDB.

### `prompt.py`

Builds the Gemini prompt using the user's question and retrieved verses.

### `download_dataset.py`

Downloads Bhagavad Gita verse data and saves it into `data/bhagavad_gita.json`.

### `streamlit_app.py`

Simple Streamlit UI for asking questions and viewing AI guidance.

### `.env`

Stores environment variables such as `GEMINI_API_KEY`.

### `requirements.txt`

Lists the Python packages needed for the project.

### `data/`

Stores the Bhagavad Gita JSON dataset.

### `chroma_db/`

Stores the local ChromaDB vector database created by `ingest.py`.
