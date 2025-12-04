from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcribe_with_groq(audio_bytes: bytes) -> str:
    result = client.audio.transcriptions.create(
        file=("audio.wav", audio_bytes),
        model="whisper-large-v3-turbo",
        response_format="text"
    )
    return result
