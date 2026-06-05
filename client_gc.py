from openai import OpenAI
import os
import time
from config import BASE_URL, MODEL

client = OpenAI(
    base_url=BASE_URL,
    api_key=os.getenv("GENERAL_COMPUTE_API_KEY"),
    timeout=120.0  # IMPORTANT: prevents your timeout crash
)

def call_gc(messages):
    start = time.time()

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )

    return {
        "text": response.choices[0].message.content,
        "latency": time.time() - start
    }