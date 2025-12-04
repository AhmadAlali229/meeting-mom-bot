from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PRO_CORRECTION = """
You are a specialist in correcting transcripts containing mixed Arabic and English
technical content. Your job:

1. Fix common Whisper transcription errors.
2. Replace broken English tech words with correct ones (so replace any arabic words thats orginally english withe the english word ) here is some examples:
   - "كومبولكت سي اشوز" → "compatibility issues"
   - "رسبونسو ديزاين" → "responsive design"
   - "ارغمونتي" → "argument"
   - "ديبلويمنت" → "deployment"
   - "التيملاين" → "timeline"
3. Add punctuation.
4. Keep meaning EXACT.
5. Do NOT invent information not said.
Return a clean, readable transcript.
"""

def clean_transcript(text: str) -> str:
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": PRO_CORRECTION},
            {"role": "user", "content": text},
        ],
        temperature=0.1,
    )

    return resp.choices[0].message.content.strip()
