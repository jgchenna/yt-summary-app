from youtube_transcript_api import YouTubeTranscriptApi
from whisper_transcribe import whisper_transcribe

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([i["text"] for i in transcript])
    except Exception:
        # Fallback to Whisper
        return whisper_transcribe(video_id)
