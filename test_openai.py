from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def test_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found.")
        return

    client = OpenAI(api_key=api_key)
    try:
        print("Testing OpenAI connection...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            max_tokens=10
        )
        print("Success! Response from AI:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"OpenAI connection failed: {e}")

if __name__ == "__main__":
    test_openai()
