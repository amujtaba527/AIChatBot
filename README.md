# Multilingual AI Voice Assistant

## Overview

This project is a multilingual AI voice assistant built in Python. It allows users to interact with an AI assistant using their voice, supporting multiple languages for both input and output. The assistant recognizes spoken language, detects the language used, generates intelligent responses using OpenAI models (via OpenRouter), and replies using natural-sounding speech.

## Features
- **Voice Recognition**: Speak to the assistant using your microphone.
- **Multilingual Support**: Detects and responds in multiple languages.
- **Conversational AI**: Uses OpenAI models for intelligent, context-aware responses.
- **Text-to-Speech**: Replies are spoken aloud using Google Text-to-Speech (gTTS).
- **Session Memory**: Maintains conversational context in a session.

## Tech Stack
- Python 3.13+
- [OpenAI API via OpenRouter](https://openrouter.ai/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangChain](https://github.com/langchain-ai/langchain)
- [gTTS (Google Text-to-Speech)](https://pypi.org/project/gTTS/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [langdetect](https://pypi.org/project/langdetect/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [playsound](https://pypi.org/project/playsound/)

## Installation

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd AIChatBot
   ```
2. **Install dependencies:**
   If you use [Poetry](https://python-poetry.org/):
   ```sh
   poetry install
   ```
   Or, using pip:
   ```sh
   pip install -r requirements.txt
   ```
   Or, using the provided `pyproject.toml`:
   ```sh
   pip install .
   ```
3. **Set up environment variables:**
   - Copy `.env.example` to `.env` and add your OpenRouter API key:
     ```env
     OPENROUTER_API_KEY=your-openrouter-api-key
     ```

## Usage

1. **Start the assistant:**
   ```sh
   python main.py
   ```
2. **Speak into your microphone when prompted.**
3. **Listen to the AI assistant's spoken response.**
4. **Press Ctrl+C to exit.**

## File Structure
- `main.py` — Main application script (voice recognition, conversation, TTS)
- `.env` — Environment variables (API keys)
- `pyproject.toml` — Python dependencies and project metadata
- `README.md` — Project documentation

## Requirements
- Python 3.13 or newer
- Microphone and speakers
- OpenRouter API key

## Credits
- Built with [OpenAI](https://openai.com/), [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://github.com/langchain-ai/langchain), [gTTS](https://pypi.org/project/gTTS/), and [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)

## License
MIT License

---

*Last updated: July 11, 2025*
