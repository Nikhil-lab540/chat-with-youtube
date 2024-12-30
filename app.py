# Import the required libraries
import tempfile
import streamlit as st
from embedchain import App

# Define the embedchain_bot function
def embedchain_bot(db_path, huggingface_api_key, groq_api_key):
    return App.from_config(
        config={
            "llm": {
                "provider": "groq",
                "config": {
                    "model": "llama3-groq-70b-8192-tool-use-preview",  # Replace with the appropriate Groq model
                    "temperature": 0.5,
                    "api_key": groq_api_key,
                },
            },
            "vectordb": {
                "provider": "chroma",
                "config": {"dir": db_path},
            },
            "embedder": {
                "provider": "huggingface",
                "config": {
                    "api_key": huggingface_api_key,
                    "model": "sentence-transformers/all-MiniLM-L6-v2",  # Example Hugging Face model
                },
            },
        }
    )

# Initialize Streamlit app
st.title("Chat with YouTube Video 📺")
st.caption("This app allows you to chat with a YouTube video using Groq for LLM and Hugging Face for embeddings")

# Step 1: Collect API keys
if "app" not in st.session_state:
    huggingface_api_key = st.text_input("Hugging Face API Key (for embedding)", type="password")
    groq_api_key = st.text_input("Groq API Key (for querying)", type="password")

    if st.button("Submit API Keys"):
        if huggingface_api_key and groq_api_key:
            # Create a temporary directory to store the database
            db_path = tempfile.mkdtemp()
            # Save the Embedchain App instance in session state
            st.session_state.app = embedchain_bot(db_path, huggingface_api_key, groq_api_key)
            st.success("API Keys successfully submitted!")
        else:
            st.warning("Please provide both API keys.")

# Step 2: Add a YouTube video
if "app" in st.session_state:
    video_url = st.text_input("Enter YouTube Video URL")
    if st.button("Add Video"):
        if video_url:
            try:
                st.session_state.app.add(video_url, data_type="youtube_video")
                st.success(f"Added {video_url} to the knowledge base!")
                st.session_state.video_added = True
            except Exception as e:
                st.error(f"Error adding video: {str(e)}")
        else:
            st.warning("Please enter a valid YouTube video URL.")

# Step 3: Ask questions about the video
if "video_added" in st.session_state and st.session_state.video_added:
    prompt = st.text_input("Ask any question about the YouTube Video")
    if st.button("Submit Question"):
        if prompt:
            try:
                answer = st.session_state.app.chat(prompt)
                st.write(answer)
            except Exception as e:
                st.error(f"Error during chat: {str(e)}")
        else:
            st.warning("Please enter a question.")
