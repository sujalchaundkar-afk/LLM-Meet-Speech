# AI Voice Assistant — Speech → LLM → Speech
A beginner-friendly complete project based on the LLMs Meet Speech concept.

## What it does
Text mode: Text → LLM → Text-to-Speech → Play/Download MP3
Voice mode: Microphone → Speech-to-Text → LLM → Text-to-Speech → Play/Download MP3
## Run locally
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Copy .env.example to .env and add your API key, then:

uvicorn app.main:app --reload
Open http://127.0.0.1:8000

## Docker
docker build -t ai-voice-assistant .
docker run --rm -p 8000:8000 --env-file .env ai-voice-assistant
## Demo
Type: "Explain Generative AI to a first-year engineering student." Click Generate Voice Response.

Then try the microphone: "What is RAG and why is it useful?"

## Learning flow
Speech → STT → LLM → TTS → Speech

The project deliberately keeps the three AI components separate so students can understand the pipeline.

## Extensions
- RAG knowledge base
- conversation history
- multiple languages
- selectable voices
- tool calling
- streaming
