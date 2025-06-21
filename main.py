import gradio as gr
from gtts import gTTS
import speech_recognition as sr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from dotenv import load_dotenv
import os

# Load env vars
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Setup LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
tools = [
    Tool(
        name="General Assistant",
        func=lambda x: "I can help with general questions.",
        description="Handles general conversation"
    )
]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=False
)

# Speech Recognition
def recognize_speech(audio_path):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)
        try:
            text = r.recognize_google(audio, language="en-US")
            return text, "en"
        except:
            text = r.recognize_google(audio, language="ur-PK")
            return text, "ur"
    except:
        return None, None

# Text to Speech using gTTS
def text_to_speech(text, lang_code):
    if not text:
        return None
    lang = "ur" if lang_code == "ur" else "en"
    tts = gTTS(text=text, lang=lang)
    tts.save("response.mp3")
    return "response.mp3"
    
# Initialize chat history outside the function to maintain state across calls
chat_history = []

# Main Logic
def process_audio(audio):
    global chat_history  # Declare chat_history as global to modify it
    if not audio:
        return "No audio provided", None
    text, lang = recognize_speech(audio)
    if not text:
        return "Could not recognize speech", None
    try:
        # Pass chat_history to the agent
        response = agent.run(input=text, chat_history=chat_history)
        # Update chat_history
        chat_history.append({"input": text, "output": response})
    except Exception as e:
        response = f"Error from LLM: {e}"
    audio_out = text_to_speech(response, lang)
    return response, audio_out

# Gradio App
interface = gr.Interface(
    fn=process_audio,
    inputs=gr.Audio(sources=["microphone", "upload"], type="filepath", label="🎙️ Speak English or Urdu"),
    outputs=[
        gr.Textbox(label="🧠 AI Response"),
        gr.Audio(label="🔊 Spoken Response")
    ],
    title="Multilingual Voice AI Assistant 🤖",
    description="Speak in English or Urdu. The AI replies in the same language."
)

interface.launch(share=True)