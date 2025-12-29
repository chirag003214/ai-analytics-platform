import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def llm(prompt: str, task: str = "insight") -> str:
    if task == "insight":
        model = "llama-3.1-8b-instant"
        max_tokens = 400
    elif task == "executive":
        model = "llama-3.1-8b-instant"
        max_tokens = 600
    elif task == "sql":
        model = "llama-3.1-8b-instant"
        max_tokens = 300
    else:
        model = "llama-3.1-8b-instant"
        max_tokens = 400

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a precise data analyst. Never hallucinate numbers."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content.strip()

