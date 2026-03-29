from groq import Groq

client = Groq(api_key="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")

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Hello"}]
)

print(response.choices[0].message.content)