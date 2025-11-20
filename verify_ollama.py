import os
from openai import OpenAI
from dotenv import load_dotenv

# Mock .env loading since we couldn't edit the real one
os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434/v1"
os.environ["OLLAMA_MODEL"] = "llama3"

base_url = os.getenv("OLLAMA_BASE_URL")
api_key = "ollama"

print(f"Connecting to {base_url}...")

try:
    client = OpenAI(base_url=base_url, api_key=api_key)
    response = client.chat.completions.create(
        model=os.getenv("OLLAMA_MODEL"),
        messages=[
            {"role": "user", "content": "Hello, are you working?"}
        ]
    )
    print("Success! Response:")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Failed to connect: {e}")
