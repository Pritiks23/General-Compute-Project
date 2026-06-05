import time
import requests
from config import VAST_URL


def call_vast(messages):
    start = time.time()

    response = requests.post(
        VAST_URL,
        json={
            "model": "llama-3-70b",
            "messages": messages
        }
    )

    latency = time.time() - start

    return {
        "text": response.json().get("choices", [{}])[0].get("message", {}).get("content", ""),
        "latency": latency
    }