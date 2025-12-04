# app/main.py
import os
from typing import List

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.mom_pipeline import (
    transcribe_audio_with_groq,
    generate_mom_with_groq,
)


app = FastAPI(
    title="Meeting MoM Bot (Groq)",
    description="Upload a meeting recording and get Minutes of Meeting (MoM) using Groq Whisper + Llama.",
    version="0.1.0",
)

# Allow all origins for dev – you can restrict later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MomResponse(BaseModel):
    meeting_title: str
    meeting_date: str
    attendees: List[str]
    transcript: str
    mom: str


@app.post("/generate-mom", response_model=MomResponse)
async def generate_mom(
    file: UploadFile = File(...),
    meeting_title: str = Form(...),
    meeting_date: str = Form(...),
    attendees: str = Form(...),  # comma-separated
):
    # Basic validation
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    # Save uploaded file to tmp folder
    try:
        contents = await file.read()
        os.makedirs("tmp", exist_ok=True)
        temp_path = os.path.join("tmp", file.filename)
        with open(temp_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # 1) Transcribe with Groq Whisper
    try:
        transcript_text = transcribe_audio_with_groq(temp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ASR (Groq Whisper) failed: {e}")

    # 2) Generate MoM with Groq LLM
    try:
        mom_text = generate_mom_with_groq(
            transcript=transcript_text,
            meeting_title=meeting_title,
            meeting_date=meeting_date,
            attendees=attendees,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM (Groq) failed: {e}")

    attendee_list = [a.strip() for a in attendees.split(",") if a.strip()]

    return MomResponse(
        meeting_title=meeting_title,
        meeting_date=meeting_date,
        attendees=attendee_list,
        transcript=transcript_text,
        mom=mom_text,
    )
