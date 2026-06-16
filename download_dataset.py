import json
import time
import urllib.request
from pathlib import Path


# Public Bhagavad Gita JSON API.
BASE_API_URL = "https://vedicscriptures.github.io/slok"

# This public API exposes 18 chapters with these verse counts.
CHAPTER_VERSES = {
    1: 47, 2: 72, 3: 43, 4: 42, 5: 29, 6: 47,
    7: 30, 8: 28, 9: 34, 10: 42, 11: 55, 12: 20,
    13: 35, 14: 27, 15: 20, 16: 24, 17: 28, 18: 78,
}

# Save the converted dataset here.
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "data" / "bhagavad_gita.json"


def download_verse(chapter, verse):
    """Download one verse from the public API."""
    url = f"{BASE_API_URL}/{chapter}/{verse}"

    # Try a few times because public APIs can sometimes be temporarily busy.
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as error:
            if attempt == 3:
                raise RuntimeError(f"Could not download {url}: {error}") from error
            print(f"Retrying Chapter {chapter}, Verse {verse}...")
            time.sleep(2)


def convert_verse(raw):
    """Convert API data into the simple project format."""
    sivananda = raw.get("siva", {})
    prabhupada = raw.get("prabhu", {})

    translation = sivananda.get("et") or prabhupada.get("et") or ""
    meaning = sivananda.get("ec") or prabhupada.get("ec") or translation

    return {
        "chapter": raw["chapter"],
        "verse": raw["verse"],
        "sanskrit": raw.get("slok", ""),
        "translation": translation.strip(),
        "meaning": meaning.strip(),
    }


def save_dataset(verses):
    """Save all verses into data/bhagavad_gita.json."""
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(verses, file, ensure_ascii=False, indent=2)


def main():
    """Download all verses, convert them, and save the JSON file."""
    verses = []

    for chapter, total_verses in CHAPTER_VERSES.items():
        for verse in range(1, total_verses + 1):
            print(f"Downloading Chapter {chapter}, Verse {verse}...")
            raw = download_verse(chapter, verse)
            verses.append(convert_verse(raw))
            time.sleep(0.2)

    save_dataset(verses)
    print(f"Saved {len(verses)} verses to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
