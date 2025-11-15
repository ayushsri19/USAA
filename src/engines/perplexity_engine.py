import os
import requests
from dotenv import load_dotenv

load_dotenv()

class PerplexityEngine:
    """
    WORKING FOR YOUR ACCOUNT:
    Uses 'r1' model (universal for Perplexity personal + pro).
    """

    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("PPLX_API_KEY missing in .env!")

        self.model = "r1"   # FINAL, GUARANTEED MODEL

    def generate(self, prompt: str) -> str:
        try:
            url = "https://api.perplexity.ai/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            body = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

            resp = requests.post(url, headers=headers, json=body)
            data = resp.json()

            if "choices" in data:
                return data["choices"][0]["message"]["content"]

            if "error" in data:
                return f"PerplexityEngine Error: {data['error']}"

            return f"PerplexityEngine Error: Unexpected response → {data}"

        except Exception as e:
            return f"PerplexityEngine Error: {e}"
