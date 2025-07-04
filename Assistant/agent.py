import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from trustcall import create_extractor

from typing import Literal, Optional, TypedDict

from langchain_core.runnables import RunnableConfig
from langchain_core.messages import merge_message_runs
from langchain_core.messages import SystemMessage, HumanMessage

from langchain_openai import ChatOpenAI

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore

from Assistant.utils import configuration

from langgraph.graph.message import MessagesState
from langgraph.graph import StateGraph, START,END
from Assistant.utils.nodes import task_mAIstro, update_profile,update_todos,update_instructions,route_message
from dotenv import load_dotenv
load_dotenv()

builder = StateGraph(MessagesState,config_schema=configuration.Configuration)

# Define the flow of the memory extraction process
builder.add_node(task_mAIstro)
builder.add_node(update_todos)
builder.add_node(update_profile)
builder.add_node(update_instructions)

# define the flow
builder.add_edge(START, "task_mAIstro")
builder.add_conditional_edges("task_mAIstro", route_message)
builder.add_edge("update_todos", "task_mAIstro")
builder.add_edge("update_profile", "task_mAIstro")
builder.add_edge("update_instructions", "task_mAIstro")



# Compile the graph
graph1 = builder.compile()

## Adding the voice capabilities 
import pyaudio

from langchain_core.messages import convert_to_messages
from langchain_core.messages import HumanMessage,SystemMessage
import io
import threading 
import numpy as np 
import sounddevice as sd
from scipy.io.wavfile import write
from openai import OpenAI
import asyncio
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

# initalizing the openAI client
openai_client = OpenAI()


async def record_audio_until_stop(state: MessagesState):
    audio_data = []
    recording = True
    sample_rate = 16000

    def record_audio():
        nonlocal audio_data, recording
        with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16') as stream:
            print("Recording... Press Enter to stop early.")
            while recording:
                chunk, _ = stream.read(1024)
                audio_data.append(chunk)  

    def stop_recording():
        input()
        nonlocal recording
        recording = False

    threading.Thread(target=record_audio).start()
    threading.Thread(target=stop_recording).start()

    while recording:
        await asyncio.sleep(0.1)

    audio_data = np.concatenate(audio_data, axis=0)
    audio_bytes = io.BytesIO()
    write(audio_bytes, sample_rate, audio_data)
    audio_bytes.seek(0)
    audio_bytes.name = "audio.wav"

    transcription = await openai_client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_bytes,
    )
    text = transcription.text.strip()
    should_stop = text.lower() in ["stop", "exit", "quit"]

    print("Transcription:", text)

    return {
        "messages": [HumanMessage(content=text)],
        "transcription": text,
        "should_stop": should_stop
    }



# Replace OpenAI with AsyncOpenAI
openai_client = AsyncOpenAI()

async def play_audio(state: MessagesState):
    """Streams and plays the audio response from OpenAI using GPT-4o-mini TTS."""
    
    # Get the most recent message
    response_msg = state['messages'][-1]
    cleaned_text = response_msg.content.replace("**", "")

    # Create a streaming response
    async with openai_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=cleaned_text,
        instructions="Speak in a cheerful and positive tone.",
        response_format="pcm",
    ) as response:
        # Use built-in helper to play the streamed audio
        await LocalAudioPlayer().play(response)

async def greet_user(state: MessagesState):
    greeting_text = "Hello! I'm your voice assistant. Tell me what you'd like me to do."
    
    async with openai_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=greeting_text,
        instructions="Speak in a cheerful and positive tone.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

    return state  # Pass unchanged state forward


def check_stop_condition(state: MessagesState):
    if state.get("should_stop"):
        print("User said stop. Ending.")
        return END
    return state
builder_1 = StateGraph(MessagesState)
# Add all nodes
builder_1.add_node("greet_user", greet_user)
builder_1.add_node("record_audio", record_audio_until_stop)
builder_1.add_node("todo_app", graph1)  # Your assistant logic
builder_1.add_node("play_audio", play_audio)
builder_1.add_node("check_stop", check_stop_condition)

# Graph flow
builder_1.set_entry_point("greet_user")
builder_1.add_edge("greet_user", "record_audio")
builder_1.add_edge("record_audio", "todo_app")
builder_1.add_edge("todo_app", "play_audio")
builder_1.add_edge("play_audio", "check_stop")
builder_1.add_edge("check_stop", "record_audio")  # loop
builder_1.add_edge("check_stop", END)

graph = builder_1.compile()

