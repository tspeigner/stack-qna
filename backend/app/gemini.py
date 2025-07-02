import os
from dotenv import load_dotenv
import httpx

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

async def generate_gemini_answer(prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(GEMINI_API_URL, headers=headers, params=params, json=data)
        response.raise_for_status()
        result = response.json()
        # Extract answer from Gemini response
        return result["candidates"][0]["content"]["parts"][0]["text"]
