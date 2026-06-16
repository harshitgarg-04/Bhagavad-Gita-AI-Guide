import requests
import streamlit as st

# FastAPI endpoint used by the Streamlit app.
API_URL = "http://localhost:8000/ask"

# Page title and short instruction.
st.title("Bhagavad Gita AI Guide")
st.write("Share a life problem and receive guidance from relevant Gita verses.")

# Text area where the user enters their question or problem.
question = st.text_area(
    "What are you struggling with?",
    placeholder="Example: I am stressed about my future",
    height=120,
)

# Submit button starts the API request.
if st.button("Ask for Guidance"):
    if not question.strip():
        st.warning("Please enter your question first.")
    else:
        try:
            # Send the user's question to the FastAPI backend.
            response = requests.post(API_URL, json={"question": question}, timeout=60)
            response.raise_for_status()
            data = response.json()

            # Display Gemini's answer.
            st.subheader("Bhagavad Gita Guidance")
            st.write(data.get("answer", "No answer returned."))

            # Display the verse references returned by the API.
            st.subheader("Relevant Bhagavad Gita Verses")
            references = data.get("references", [])
            if references:
                for item in references:
                    chapter = item.get("chapter", "")
                    verse = item.get("verse", "")
                    st.write(f"- Chapter {chapter}, Verse {verse}")
            else:
                st.write("No verse references returned.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the FastAPI server.")
        except requests.exceptions.Timeout:
            st.error("The request took too long. Please try again.")
        except requests.exceptions.RequestException as error:
            st.error(f"API error: {error}")
