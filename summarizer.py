from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(transcript):
    prompt = f"""
    Summarize the following YouTube transcript.

    Return:
    1. Short paragraph summary
    2. 5 key bullet points

    Transcript:
    {transcript}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You summarize videos clearly."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
