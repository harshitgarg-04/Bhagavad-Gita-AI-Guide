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

# Execution Steps

1. Create a Virtual Environment

python -m venv venv

venv\Scripts\activate

2. Install Dependencies

pip install -r requirements.txt

3. Create a .env File

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key

4. Download Bhagavad Gita Dataset

python download_dataset.py

This creates:

data/bhagavad_gita.json

5. Create Vector Database

Generate embeddings and store them in ChromaDB:

python ingest.py

This creates:

chroma_db/

6. Start FastAPI Backend

uvicorn app:app --reload

Backend runs at:

http://127.0.0.1:8000

7. Run Streamlit Frontend

Open a new terminal and run:

streamlit run streamlit_app.py

Streamlit opens at:

http://localhost:8501
