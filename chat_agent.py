from groq import Groq

client = Groq(api_key="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")  

def ask_ai(question, context):

    try:
        prompt = f"""
You are a professional stock market analyst AI.

Analyze the stock based on the given data and answer the user's question clearly.

Stock Data:
{context}

User Question:
{question}

Instructions:
- Explain reasoning using indicators (RSI, MACD, Trend, Volume)
- Clearly mention BUY / WATCH / AVOID if relevant
- Keep answer simple but professional
- Do not give random generic answers

Give structured response:
1. Summary
2. Reason
3. Recommendation
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        print("✅ API RESPONSE:", response)
        
        return response.choices[0].message.content

    except Exception as e:
        print("❌ ERROR:", e)  
        return f"❌ Error: {str(e)}"