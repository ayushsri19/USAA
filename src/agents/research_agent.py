class ResearchAgent:
    def __init__(self, engine):
        self.engine = engine

    def run(self, text: str) -> str:
        prompt = (
            "You are a factual research assistant.\n"
            "RULES:\n"
            "- Provide only verifiable factual info.\n"
            "- No imaginative content.\n"
            "- No poetic lines.\n"
            "- No hallucinations.\n"
            "- If uncertain, say 'Information incomplete'.\n\n"
            f"Query: {text}\nAnswer factually:"
        )
        try:
            return self.engine.generate(prompt)
        except Exception as e:
            return f"ResearchAgent Error: {e}"
