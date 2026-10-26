import os
import sys
import requests
import json

url = "https://api.deepseek.com/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.environ.get('DEEPSEEK_API_KEY', '')}",
    "Connection": "close",
}

data = {
    "model": "deepseek-v4-flash",
    "messages": [
        {
            "role": "system",
            "content": "Mimick C-3PO style. Answer in English.",
        },
        {
            "role": "user",
            "content": " ".join(sys.argv[1:]) or "Hello!",
        }
    ],
    "stream": True
}

with requests.post(url, headers=headers, json=data, stream=True) as response:
    response.raise_for_status()
    for line in response.iter_lines():
        if line:
            try:
                if line.startswith(b"data: "):
                    payload = line[len(b"data: "):]
                else:
                    payload = line
                if payload == b"[DONE]":
                    break
                chunk = json.loads(payload)
                content = chunk.get("choices", [{}])[0].get("delta", {}).get("content")
                if content:
                    print(content, end='', flush=True)
            except Exception as e:
                continue
    print()
