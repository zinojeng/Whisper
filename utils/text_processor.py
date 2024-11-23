from typing import List
from .openai_client import create_chat_completion
from config.settings import MAX_TEXT_LENGTH

def split_text(text: str, max_length: int = MAX_TEXT_LENGTH) -> List[str]:
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def process_text(client, text: str, system_prompt: str) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Please summarize the following text in 500 words as detail as you can in zh-tw: {text}"}
    ]
    return create_chat_completion(client, messages)

def translate_text(client, text: str, system_prompt: str, to_language: str = "zh-tw") -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Translate the following English text to {to_language}: {text}"}
    ]
    return create_chat_completion(client, messages)

def summarize_text(client, text: str, system_prompt: str) -> List[str]:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Summarize the following text into 10 key points in zh-tw: {text}"}
    ]
    response = create_chat_completion(client, messages)
    return response.split('\n')[:10]
