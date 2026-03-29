import os
from dotenv import load_dotenv
from groq import Groq

# 🔐 Load environment variables
load_dotenv()

# 🔑 Get API key
api_key = os.getenv("GROQ_API_KEY")

# ⚠️ Safe client initialization
client = None
if api_key:
    client = Groq(api_key=api_key)


def ask_ai(prompt, context=""):
    """
    Generate AI response using Groq
    """

    # ❗ If API key missing
    if client is None:
        return "⚠️ API key not found. Please set GROQ_API_KEY in .env"

    try:
        full_prompt = f"""
You are a financial AI assistant.

Context:
{context}

User Question:
{prompt}

Instructions:
- Give clear and simple answer
- If stock related, explain briefly
- Keep it concise
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful financial assistant."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"
