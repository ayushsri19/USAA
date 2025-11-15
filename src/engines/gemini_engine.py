# src/engines/gemini_engine.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class GeminiEngine:
    def __init__(self):
        key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError("GEMINI_API_KEY missing in .env!")

        genai.configure(api_key=key)

        # SAFE MODELS
        self.model_name = "gemini-2.5-flash"     # fast + reliable
        self.model = genai.GenerativeModel(self.model_name)

    def generate(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"GeminiEngine Error: {e}"
