import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException

from dotenv import load_dotenv
load_dotenv()

from app.pipeline.asr import transcribe_with_groq
from app.pipeline.cleaner import clean_transcript
from app.pipeline.mom import generate_mom
from app.pipeline.diarization import diarize_audio_api  # optional


app = FastAPI(
    title="Meeting MoM Bot (Whisper Only)",
    description="Generate MoM using Groq Whisper + Llama 70B (No Enhancement)",
    version="1.0"
)


@app.post("/generate-mom")
async def generate_mom_api(
    file: UploadFile = File(...),
    meeting_title: str = Form(...),
    meeting_date: str = Form(...),
    attendees: str = Form(...)
):

    if not file.filename:
        raise HTTPException(400, "Missing audio file")

    raw_path = f"tmp/{file.filename}"
    os.makedirs("tmp", exist_ok=True)
    contents = await file.read()

    with open(raw_path, "wb") as f:
        f.write(contents)

    # 1) Speaker Diarization (Optional — if fails, ignore)
    diarized_text = ""
    try:
        audio_bytes = open(raw_path, "rb").read()
        diarized_segments = diarize_audio_api(audio_bytes)

        diarized_text = "\n".join(
            [f"Speaker {seg['speaker']}: {seg['text']}" for seg in diarized_segments]
        )
    except:
        diarized_text = ""

    # 2) ASR (Whisper via Groq)
    try:
        raw_text = transcribe_with_groq(open(raw_path, "rb").read())
    except Exception as e:
        raise HTTPException(500, f"ASR failed: {e}")

    # Combine diarization + transcription
    combined = (diarized_text + "\n" + raw_text).strip()

    # 3) Clean transcript
    cleaned = clean_transcript(combined)

    # 4) Generate MoM
    mom = generate_mom(cleaned, meeting_title, meeting_date, attendees)

    return {
        "diarized_transcript": diarized_text,
        "raw_transcript": raw_text,
        "clean_transcript": cleaned,
        "mom": mom
    }
