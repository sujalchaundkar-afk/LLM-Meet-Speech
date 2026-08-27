from pathlib import Path
from uuid import uuid4
from app.services.openai_client import client, LLM_MODEL, TRANSCRIPTION_MODEL, TTS_MODEL, TTS_VOICE

AUDIO_DIR = Path("data/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

SYSTEM_PROMPT = (
    "You are a helpful AI voice assistant for college students. "
    "Answer clearly and naturally. Keep responses concise enough to be comfortable when spoken aloud. "
    "Avoid unnecessary markdown and tables."
)

def transcribe_audio(audio_path: Path) -> str:
    with audio_path.open("rb") as f:
        result = client.audio.transcriptions.create(model=TRANSCRIPTION_MODEL, file=f)
    return result.text.strip()

def answer_from_text(user_text: str) -> str:
    response = client.responses.create(
        model=LLM_MODEL,
        instructions=SYSTEM_PROMPT,
        input=user_text,
    )
    return response.output_text.strip()

def generate_speech(text: str) -> Path:
    output = AUDIO_DIR / f"response_{uuid4().hex}.mp3"
    with client.audio.speech.with_streaming_response.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=text,
        response_format="mp3",
    ) as response:
        response.stream_to_file(output)
    return output
