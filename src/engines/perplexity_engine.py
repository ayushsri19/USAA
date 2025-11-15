import os
import requests

class PerplexityEngine:
    """
    SAFE-MODE enabled — missing key = engine disabled (no error)
    """

    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY") or os.getenv("PPLX_API_KEY")

        if not self.api_key:
            self.enabled = False
            return

        self.enabled = True
        self.model = "r1"

    def generate(self, prompt: str) -> str:
        if not self.enabled:
            return "(Perplexity disabled: no API key)"

        try:
            url = "https://api.perplexity.ai/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            body = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}]
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
