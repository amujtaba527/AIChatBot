import os
import time
from openai import OpenAI
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
import speech_recognition as sr
from gtts import gTTS
from langdetect import detect
from dotenv import load_dotenv
import playsound

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("API key not found. Make sure OPENROUTER_API_KEY is set in your .env file.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)
 
def call_model(state: MessagesState):
    # Convert LangChain messages to OpenAI-style dicts
    messages = []
    for msg in state["messages"]:
        if isinstance(msg, HumanMessage):
            messages.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            messages.append({"role": "assistant", "content": msg.content})
        else:
            print("Skipping unknown message type:", msg)

    response = client.chat.completions.create(
        model="meta-llama/llama-3.3-8b-instruct:free",
        messages=messages
    )
    return {"messages": [AIMessage(content=response.choices[0].message.content.strip())]}


workflow = StateGraph(state_schema=MessagesState)
workflow.add_node("model", call_model)
workflow.add_edge(START, "model")
app = workflow.compile(checkpointer=MemorySaver())

# 🎤 Speech recognition function
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎙️ Speak now...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            lang = detect(text)
            lang = "en"
            return text, lang
        except sr.UnknownValueError:
            return None, None
        except Exception as e:
            print(f"Speech error: {str(e)}")
            return None, None

# 🗣️ Text-to-speech function
def speak(text, lang_code):
    try:
        tts = gTTS(text, lang=lang_code, slow=False)
        filename = f"reply_{int(time.time())}.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
    except Exception as e:
        print(f"TTS error: {str(e)}")

# 🚀 Main loop
if __name__ == "__main__":
    print("\n🤖 Multilingual Voice Assistant")
    print("Press Ctrl+C to exit.")

    conversation_id = "user-session"
    chat_history = []

    while True:
        text, lang = recognize_speech()
        if not text:
            print("Could not understand. Try again.")
            continue

        print(f"You ({lang}):", text)

        # Add user message
        chat_history.append(HumanMessage(content=text))

        # Call the assistant
        output = app.invoke(
            {"messages": chat_history},
            config={"configurable": {"thread_id": conversation_id}}
        )

        ai_reply = output["messages"][-1].content
        print("Assistant:", ai_reply)
        chat_history.append(output["messages"][-1])

        # Speak out the response
        speak(ai_reply, lang)
