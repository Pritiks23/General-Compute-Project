from openai import OpenAI
import os

print("1. Script started")

client = OpenAI(
    base_url=os.getenv("GENERAL_COMPUTE_URL"),
    api_key=os.getenv("GENERAL_COMPUTE_API_KEY"),
)

print("2. Client created")

try:
    print("3. Sending request...")

    response = client.chat.completions.create(
        model="minimax-m2.7",
        messages=[
            {"role": "user", "content": "Say 'benchmark working' in one line"}
        ],
    )

    print("4. Got response object")
    print(response)

    print("\n5. Parsed output:\n")
    print(response.choices[0].message.content)

except Exception as e:
    print("\n❌ ERROR OCCURRED:\n")
    print(type(e))
    print(e)