import os
from openai import OpenAI

class OpenAIEngine:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            self.enabled = False
            return

        self.enabled = True
        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str) -> str:
        if not self.enabled:
            return "(OpenAI disabled: no API key)"

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=300
            )
            return response.choices[0].message.content

        except Exception as e:
            return f"OpenAIEngine Error: {e}"
