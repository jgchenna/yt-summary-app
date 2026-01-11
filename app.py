import streamlit as st
from transcript import get_transcript
from summarizer import summarize_text
from utils import extract_video_id

st.set_page_config(page_title="YouTube Summary AI", layout="centered")

st.title("🎥 YouTube Video Summarizer")
st.write("Paste a YouTube link and get an AI-generated summary.")

url = st.text_input("YouTube Video URL")

if st.button("Generate Summary"):
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
                summary = summarize_text(transcript)

            st.success("Summary ready")
            st.markdown(summary)