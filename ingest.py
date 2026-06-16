import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# Basic project paths.
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "bhagavad_gita.json"
CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "bhagavad_gita"


def load_verses():
    """Load verses from the Bhagavad Gita JSON file."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Could not find data file: {DATA_FILE}")
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
    # This beginner version expects a list of verse objects.
    if not isinstance(data, list):
        raise ValueError("bhagavad_gita.json must contain a list of verses.")
    return data


def make_text(verse):
    """Convert one verse dictionary into searchable text."""
    chapter = verse.get("chapter", "")
    verse_number = verse.get("verse", "")
    sanskrit = verse.get("sanskrit", "")
    translation = verse.get("translation", "")
    meaning = verse.get("meaning", "")
    return (
        f"Chapter {chapter}, Verse {verse_number}\n"
        f"Sanskrit: {sanskrit}\n"
        f"Translation: {translation}\n"
        f"Meaning: {meaning}"
    )


def main():
    """Create embeddings and store them in ChromaDB."""
    print("Loading Bhagavad Gita verses...")
    verses = load_verses()
    if not verses:
        raise ValueError("No verses found in bhagavad_gita.json.")

    # Convert each verse into plain text for embedding.
    documents = [make_text(verse) for verse in verses]

    # Create simple IDs like verse_1, verse_2, verse_3.
    ids = [f"verse_{i + 1}" for i in range(len(documents))]

    # Store chapter and verse numbers as metadata for later display.
    metadatas = [{
        "chapter": str(verse.get("chapter", "")),
        "verse": str(verse.get("verse", "")),
    } for verse in verses]

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Creating embeddings...")
    embeddings = model.encode(documents).tolist()

    print("Saving embeddings to ChromaDB...")
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    collection.add(ids=ids, documents=documents,
                   embeddings=embeddings, metadatas=metadatas)
    print(f"Done! Saved {len(documents)} verses to ChromaDB.")


if __name__ == "__main__":
    main()
