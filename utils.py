import re

def extract_video_id(url):
    # Match video ID from youtube.com/watch?v=ID or youtu.be/ID
    # Stop at any query parameter (&, ?, etc.)
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]+)", url)
    return match.group(1) if match else None
