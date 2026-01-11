import os
import yt_dlp
from openai import OpenAI

def download_audio(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    output_template = f"%(id)s.%(ext)s"
    
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "quiet": False,
        "no_warnings": False,
    }

    # Only set FFmpeg location if explicitly provided
    #ffmpeg_loc = os.getenv("FFMPEG_PATH")
    #if ffmpeg_loc:
    #    ydl_opts["ffmpeg_location"] = ffmpeg_loc

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # Get the actual filename that was created
        audio_file = ydl.prepare_filename(info)
    
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"Audio file not found: {audio_file}")
    
    return audio_file

def whisper_transcribe(video_id, api_key):
    """Download audio and transcribe via OpenAI Speech-to-Text API.

    This avoids importing the local `whisper` package which can fail on Windows.
    """
    client = OpenAI(api_key=api_key)
    audio_file = download_audio(video_id)
    text = ""
    try:
        with open(audio_file, "rb") as f:
            resp = client.audio.transcriptions.create(file=f, model="whisper-1")
            # resp is a Transcription object with a .text attribute
            text = resp.text
    finally:
        try:
            os.remove(audio_file)
        except Exception:
            pass

    return text
