import streamlit as st
from transcript import get_transcript
from summarizer import summarize_text
from utils import extract_video_id

st.set_page_config(page_title="YouTube Summary AI", layout="centered")

st.title("🎥 YouTube Video Summarizer")
st.write("Paste a YouTube link and get an AI-generated summary.")

# API Key input in sidebar
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter OpenAI API Key", type="password", key="openai_api_key")

url = st.text_input("YouTube Video URL")

if st.button("Generate Summary"):
    if not api_key:
        st.error("Please enter your OpenAI API Key in the sidebar.")
    else:
        video_id = extract_video_id(url)

        if not video_id:
            st.error("Invalid YouTube URL")
        else:
            with st.spinner("Fetching transcript (Whisper fallback may take ~1 minute)..."):
                    transcript = get_transcript(video_id)

            if not transcript or len(transcript.strip()) < 50:
                st.error("Unable to extract transcript from this video.")
            else:
                with st.spinner("Generating AI summary..."):
                    summary = summarize_text(transcript, api_key)

                st.success("Summary ready")
                st.markdown(summary)