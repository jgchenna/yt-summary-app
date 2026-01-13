from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transcript import get_transcript
from utils import extract_video_id

app = FastAPI()


class TranscriptRequest(BaseModel):
    url: str
    api_key: str


class TranscriptResponse(BaseModel):
    transcript: str


@app.get("/")
def read_root():
    return {"message": "Welcome to YouTube Transcript API"}


@app.post("/transcript", response_model=TranscriptResponse)
def get_transcript_endpoint(request: TranscriptRequest):
    """
    Get transcript from a YouTube video.
    
    - **url**: YouTube video URL
    - **api_key**: API key for Whisper fallback
    """
    try:
        video_id = extract_video_id(request.url)
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        transcript = get_transcript(video_id, request.api_key)
        return TranscriptResponse(transcript=transcript)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
