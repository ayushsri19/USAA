class LogicAgent:
    def __init__(self, engine):
        self.engine = engine

    def run(self, text: str) -> str:
        prompt = (
            "You are a logical, step-by-step solver. "
            "Explain reasoning briefly and give final answer.\n"
            f"Question: {text}"
        )
        try:
            return self.engine.generate(prompt)
        except Exception as e:
            return f"LogicAgent Error: {e}"
