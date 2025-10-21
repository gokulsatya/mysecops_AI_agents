import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in .env file.")

# Create a chat-based request using the new API
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an assistant that enriches security alerts."},
        {"role": "user", "content": "Provide a summary of this alert: Failed SSH login from IP 192.168.1.1."}
    ]
)

# Print the response
print("Response from OpenAI API:")
print(response["choices"][0]["message"]["content"].strip())
