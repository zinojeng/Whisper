from openai import OpenAI
from typing import List
from tempfile import NamedTemporaryFile

class AudioProcessor:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        
def init_openai(api_key: str):
    return OpenAI(api_key=api_key)

def create_chat_completion(client: OpenAI, messages: List[dict], model: str = "gpt-4") -> str:
    """
    使用指定的模型創建聊天完成
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content.strip()

def create_transcription(client: OpenAI, audio_file) -> str:
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="en"
    )
    return transcription.text
