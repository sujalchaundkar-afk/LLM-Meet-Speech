from pathlib import Path
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.services.voice_pipeline import answer_from_text, transcribe_audio, generate_speech

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="AI Voice Assistant", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

class TextRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/text")
def text_pipeline(request: TextRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Please enter some text.")
    answer = answer_from_text(text)
    audio = generate_speech(answer)
    return {"transcript": text, "answer": answer, "audio_url": f"/api/audio/{audio.name}"}

@app.post("/api/voice")
async def voice_pipeline(audio: UploadFile = File(...)):
    if not audio.filename:
        raise HTTPException(status_code=400, detail="Audio file is required.")
    suffix = Path(audio.filename).suffix or ".webm"
    temp = Path("data") / f"input{suffix}"
    temp.parent.mkdir(exist_ok=True)
    try:
        temp.write_bytes(await audio.read())
        transcript = transcribe_audio(temp)
        answer = answer_from_text(transcript)
        output = generate_speech(answer)
        return {"transcript": transcript, "answer": answer, "audio_url": f"/api/audio/{output.name}"}
    finally:
        temp.unlink(missing_ok=True)

@app.get("/api/audio/{filename}")
def get_audio(filename: str):
    path = Path("data/audio") / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="Audio not found.")
    return FileResponse(path, media_type="audio/mpeg", filename=filename)
