import openai
import streamlit as st
import os

st.title("Audio to Text")

# Get the open AI API Key
api_key = st.text_input(label="OpenAI API Key", placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key", help="You can get your API key from https://platform.openai.com/account/api-keys/")
os.environ["OPENAI_API_KEY"] = api_key

# File uploader
audio = st.file_uploader(label="Upload audio file", type=['wav', 'mp3', 'm4a'])

if audio is not None:
#   mediafile = open('media_file', 'r')
   response = openai.Audio.transcribe("whisper-1", audio, verbose=True, api_key=api_key)
   st.write(response["text"])