import requests
import os
from dotenv import load_dotenv
load_dotenv()


def diarize_audio_api(audio_bytes: bytes) -> list:
    url = "https://api.deepgram.com/v1/listen?diarize=true"
    headers = {
        "Authorization": f"Token {os.getenv('DEEPGRAM_API_KEY')}",
        "Content-Type": "audio/wav",
    }

    response = requests.post(url, headers=headers, data=audio_bytes)

    if response.status_code != 200:
        raise RuntimeError(f"Diarization error: {response.text}")

    results = response.json()

    segments = []
    for channel in results["results"]["channels"]:
        for alt in channel["alternatives"]:
            for para in alt.get("paragraphs", {}).get("paragraphs", []):
                segments.append({
                    "speaker": para["speaker"],
                    "text": para["transcript"]
                })
    return segments
