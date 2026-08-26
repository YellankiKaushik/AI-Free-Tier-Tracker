from __future__ import annotations

import json
import os

import requests

BASE = os.getenv('OLLAMA_URL','http://127.0.0.1:11434').rstrip('/')
MODEL = os.getenv('OLLAMA_MODEL','gemma3:4b')

def extract_json(system: str, user: str, timeout: int = 180) -> dict:
    payload = {
        'model': MODEL,
        'stream': False,
        'format': 'json',
        'messages': [
            {'role':'system','content':system},
            {'role':'user','content':user},
        ],
        'options': {'temperature': 0.0}
    }
    r = requests.post(f'{BASE}/api/chat', json=payload, timeout=timeout)
    r.raise_for_status()
    content = r.json()['message']['content']
    return json.loads(content)
