from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_mom(text: str, title: str, date: str, attendees: str):
    prompt = f"""
Meeting Title: {title}
Date: {date}
Attendees: {attendees}

Transcript:
{text}

Write a professional Minutes of Meeting with:
- Agenda
- Discussion Summary
- Decisions
- Action Items
"""
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You generate MoM in clear structured format."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()
