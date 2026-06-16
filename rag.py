from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# Use the same folder and collection name as ingest.py.
BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "bhagavad_gita"
MODEL_NAME = "all-MiniLM-L6-v2"


def get_value(document, label):
    """Find a line like 'Translation: text' inside the saved document."""
    for line in document.splitlines():
        if line.startswith(label + ":"):
            return line.split(":", 1)[1].strip()
    return ""


def search_verses(question: str):
    """Search ChromaDB and return the top 3 relevant Bhagavad Gita verses."""
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    try:
        # Load the same embedding model used during ingestion.
        model = SentenceTransformer(MODEL_NAME)

        # Connect to the local ChromaDB database.
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        collection = client.get_collection(name=COLLECTION_NAME)

        # Convert the user's question into an embedding.
        question_embedding = model.encode(question).tolist()

        # Ask ChromaDB for the 3 closest stored verses.
        results = collection.query(query_embeddings=[question_embedding],
                                   n_results=3)
    except Exception as error:
        raise RuntimeError(f"Could not search verses: {error}") from error

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    verses = []
    for document, metadata in zip(documents, metadatas):
        # Metadata has chapter and verse; document has translation and meaning.
        verses.append({"chapter": metadata.get("chapter", ""),
                       "verse": metadata.get("verse", ""),
                       "translation": get_value(document, "Translation"),
                       "meaning": get_value(document, "Meaning")})
    return verses


if __name__ == "__main__":
    user_question = input("Ask a life question: ")
    for verse in search_verses(user_question):
        print(verse)
