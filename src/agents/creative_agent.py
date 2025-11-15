from datetime import datetime

class CreativeAgent:
    def __init__(self, engine):
        self.engine = engine

    def run(self, text: str) -> str:
        t = text.lower()

        # universal real-world queries (never hallucinate)
        if "date" in t:
            return datetime.now().strftime("%d %B %Y")

        if "day" in t:
            return datetime.now().strftime("%A")

        if "time" in t:
            return datetime.now().strftime("%I:%M %p")

        # no hallucination creative mode
        prompt = (
            "You are a controlled creative assistant.\n"
            "RULES:\n"
            "- No hallucinations.\n"
            "- No fake facts.\n"
            "- No guessing.\n"
            "- Only answer based on user’s topic.\n"
            "- If unsure, say 'I don’t know'.\n\n"
            f"User: {text}\n"
            "Answer:"
        )

        try:
            return self.engine.generate(prompt)
        except Exception as e:
            return f"CreativeAgent Error: {e}"
