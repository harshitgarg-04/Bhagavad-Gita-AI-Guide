def build_prompt(question, context):
    """Build a Gemini prompt using the user's question and retrieved verses."""

    # Convert each retrieved verse into readable context for Gemini.
    verse_texts = []
    for item in context:
        verse_texts.append(
            f"Chapter {item.get('chapter', '')}, Verse {item.get('verse', '')}\n"
            f"Translation: {item.get('translation', '')}\n"
            f"Meaning: {item.get('meaning', '')}"
        )

    # Join all verses into one context block.
    verses_block = "\n\n".join(verse_texts)

    # This prompt tells Gemini to stay grounded in the given verses only.
    prompt = f"""
You are a Bhagavad Gita life guidance assistant.

User question:
{question}

Retrieved Bhagavad Gita verses:
{verses_block}

Instructions:
- Use ONLY the provided verses.
- Do not invent or quote any verse that is not provided.
- Explain the meaning in simple beginner-friendly language.
- Give practical life advice based on the provided verses.
- Mention the chapter and verse numbers in your answer.
- If the verses are not enough, say that the provided verses are limited.

Answer:
"""

    return prompt.strip()
