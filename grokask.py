import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

XAI_API_KEY = os.getenv("XAI_API_KEY")

if not XAI_API_KEY:
    raise ValueError("XAI_API_KEY not found in environment variables")

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

def ask_grok(question):
    completion = client.chat.completions.create(
        model="grok-beta",
        messages=[
            {"role": "system", "content": "You are Grok, an AI assistant with a witty personality. You aim to be helpful while maintaining a sense of humor."},
            {"role": "user", "content": question},
        ],
    )
    
    return completion.choices[0].message.content

# Example usage
if __name__ == "__main__":
    while True:
        user_input = input("\nAsk Grok something (or type 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
            
        response = ask_grok(user_input)
        print("\nGrok:", response)
