import os

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from prompt import build_prompt
from rag import search_verses


# Load environment variables from the .env file.
load_dotenv()

# Read the Gemini API key from .env.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


# Create the FastAPI app.
app = FastAPI(title="Bhagavad Gita AI Guide")


class AskRequest(BaseModel):
    """The JSON body expected by POST /ask."""
    question: str


@app.get("/health")
def health():
    """Simple endpoint to check if the API is running."""
    return {"status": "ok"}


@app.post("/ask")
def ask(request: AskRequest):
    """Answer a user question using RAG plus Gemini."""
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API key not found.")

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        # Step 1: Search ChromaDB for relevant Bhagavad Gita verses.
        verses = search_verses(request.question)

        # Step 2: Build a safe prompt using only retrieved verses.
        prompt = build_prompt(request.question, verses)

        # Step 3: Send the prompt to Gemini.
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        # Step 4: Return Gemini's answer and verse references.
        references = [
            {"chapter": item["chapter"], "verse": item["verse"]}
            for item in verses
        ]

        return {"answer": response.text, "references": references}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
