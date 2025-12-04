import base64
import requests
import os
import tempfile
import subprocess


def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video to WAV for Audo.ai."""
    temp_wav = os.path.join(tempfile.gettempdir(), "converted.wav")

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ac", "1",
        "-ar", "16000",
        temp_wav,
    ]

    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return temp_wav


def enhance_audio_api(input_path: str) -> bytes:
    api_key = os.getenv("AUDO_API_KEY")
    url = "https://api.audo.ai/v1/enhance"

    wav_path = convert_to_wav(input_path)

    # Read WAV as bytes then encode to base64
    with open(wav_path, "rb") as f:
        audio_bytes = f.read()
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    payload = {
        "input": audio_b64,   # Base64 content
        "format": "wav",
        "sample_rate": 16000
    }

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"Audo Enhancement error: {response.text}")

    json_resp = response.json()

    # Enhanced audio returned as Base64 too
    enhanced_b64 = json_resp["result"]["enhanced"]

    enhanced_audio = base64.b64decode(enhanced_b64)

    return enhanced_audio
