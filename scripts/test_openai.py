import openai

# Replace "your-api-key" with your OpenAI API key
openai.api_key = "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"

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
