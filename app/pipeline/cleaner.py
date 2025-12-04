from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def clean_transcript(text: str) -> str:
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You clean transcript. Fix spacing & punctuation. Keep Arabic intact."},
            {"role": "user", "content": text},
        ],
        temperature=0.0,
    )
    return resp.choices[0].message.content.strip()
