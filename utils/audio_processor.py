from tempfile import NamedTemporaryFile
from typing import List
from .openai_client import create_transcription
from config.settings import CHUNK_SIZE

def split_audio(audio_data) -> List:
    return [
        audio_data[i:i + CHUNK_SIZE]
        for i in range(0, len(audio_data), CHUNK_SIZE)
    ]

def process_audio_chunks(chunks: List) -> str:
    transcript = ""
    for chunk in chunks:
        with NamedTemporaryFile(suffix=".wav", delete=True) as f:
            chunk.export(f.name, format="wav")
            with open(f.name, "rb") as audio_file:
                transcript += create_transcription(audio_file)
    return transcript 