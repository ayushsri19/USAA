import os
import google.generativeai as genai

class GeminiEngine:
    def __init__(self):
        key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

        if not key:
            self.enabled = False
            return

        self.enabled = True
        genai.configure(api_key=key)

        self.model_name = "gemini-2.5-flash"
        self.model = genai.GenerativeModel(self.model_name)

    def generate(self, prompt: str) -> str:
        if not self.enabled:
            return "(Gemini disabled: no API key)"

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"GeminiEngine Error: {e}"
