import streamlit as st
from dotenv import load_dotenv
import os
import requests
from urllib.parse import quote


# Load API keys

load_dotenv()


# Movie info function

def get_movie_info(title: str) -> str:
    """Fetch movie information from OMDb API."""
    api_key = os.getenv("OMDB_API_KEY")
    if not api_key:
        return "OMDB_API_KEY not found in .env file."
    
    # URL encode movie title
    url = f"http://www.omdbapi.com/?t={quote(title)}&apikey={api_key}"
    
    try:
        data = requests.get(url).json()
        if data.get("Response") == "False":
            return f"Movie not found: {title}"
        return (
            f"🎬 Title: {data['Title']}\n"
            f"📅 Year: {data['Year']}\n"
            f"🎭 Genre: {data['Genre']}\n"
            f"🎬 Director: {data['Director']}\n"
            f"📝 Plot: {data['Plot']}"
        )
    except Exception as e:
        return f"Movie service error: {e}"

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Movie Info Chatbot", page_icon="🎬")
st.title("🎬 Movie Info Chatbot")
st.caption("Enter a movie name – get info instantly")

# Initialize chat session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"].replace("\n", "\n\n"))

# Take new user input
if prompt := st.chat_input("Enter movie name (e.g. Inception, Titanic)"):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Fetch movie info and display
    with st.chat_message("assistant"):
        with st.spinner("Fetching movie info..."):
            reply = get_movie_info(prompt)
            st.markdown(reply.replace("\n", "\n\n"))
            st.session_state.messages.append({"role": "assistant", "content": reply})
