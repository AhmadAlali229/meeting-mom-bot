from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

WHISPER_TECH_PROMPT = """
You are transcribing a meeting with mixed Arabic + English technical terminology.
Preferred English technical terms include:
API, frontend, backend, compatibility issues, responsive design, integration,
deploy, authentication, argument, timeline, debugging, testing, production.

Use correct English spellings when heard.
"""

def transcribe_with_groq(audio_bytes: bytes) -> str:
    result = client.audio.transcriptions.create(
        file=("audio.wav", audio_bytes),
        model="whisper-large-v3-turbo",

        # Whisper internal tuning (allowed params ONLY)
        temperature=0,                # أقل عشوائية
        language="ar",                # يمنع التخمين ويحسن العربي المختلط
        prompt=WHISPER_TECH_PROMPT,   # يساعد Whisper يفهم الكلمات التقنية
        response_format="text"
    )

    return result
