import logging
import re
import unicodedata

log = logging.getLogger("usaa.router")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(name)s:%(message)s")


class Router:
    def __init__(self, engines: dict):
        self.engines = engines

        from src.agents.creative_agent import CreativeAgent
        from src.agents.logic_agent import LogicAgent
        from src.agents.research_agent import ResearchAgent

        self.creative_agent = CreativeAgent(self.engines.get("openai"))   # OpenAI → Creative + Research default
        self.logic_agent = LogicAgent(self.engines.get("gemini"))         # Gemini → Logic + fallback research
        self.perplexity_agent = ResearchAgent(self.engines.get("perplexity"))  # Perplexity → only worst-case fallback

    # -------------------------------------------------------
    # 1) Advanced NLP Normalizer (removes noise, punctuation,
    #    accents, normalizes unicode, lowercasing, cleaning)
    # -------------------------------------------------------
    def normalize(self, text: str) -> str:
        t = text.lower().strip()

        # Unicode normalization (removes weird chars)
        t = unicodedata.normalize("NFKD", t)

        # Extra spaces remove
        t = " ".join(t.split())

        # Remove punctuation for cleaner intent detection
        t = re.sub(r"[^\w\s]", "", t)

        return t

    # -------------------------------------------------------
    # 2) Identity Override (strong, unbreakable)
    # -------------------------------------------------------
    def identity_override(self, text: str) -> str:
        t = self.normalize(text)

        keywords = [
            "who created you",
            "who created u",
            "who made you",
            "who made u",
            "who built you",
            "who built u",
            "who coded you",
            "who coded u",
            "who developed you",
            "who developed u",
            "your creator",
            "your developer",
            "kisne banaya",
            "kisne banayi",
            "kisne tumhe",
            "kisne create",
        ]

        for k in keywords:
            if k in t:
                return "Ayush Srivastava created me."

        return None

    # -------------------------------------------------------
    # 3) Terminal Command Blocker
    # -------------------------------------------------------
    def is_terminal_command(self, text: str) -> bool:
        terminal_keywords = [
            "python", "activate", "venv", "cd", "dir",
            "pip", "ps1", "exe", "&", "./", "rm", "mv"
        ]
        return any(k in text.lower() for k in terminal_keywords)

    # -------------------------------------------------------
    # 4) Intent Detection (using proper NLP)
    # -------------------------------------------------------
    def detect_intent(self, text: str) -> str:
        t = self.normalize(text)

        if self.is_terminal_command(t):
            return "ignore"

        # Logic
        logic_words = ["solve", "logic", "calculate", "math", "derive", "compute"]
        if any(w in t for w in logic_words):
            return "logic"

        # Research (OpenAI → Gemini fallback)
        research_words = ["who", "what", "where", "when", "why", "history", "fact", "research", "explain"]
        if any(w in t.split() for w in research_words):
            return "research"

        # Creative (default)
        return "creative"

    # -------------------------------------------------------
    # 5) Final Handler
    # -------------------------------------------------------
    def handle(self, text: str) -> str:

        # Identity override (always first)
        identity = self.identity_override(text)
        if identity:
            return identity

        intent = self.detect_intent(text)

        # Ignore terminal commands silently
        if intent == "ignore":
            return ""

        try:
            # Logic → Gemini only
            if intent == "logic":
                return self.logic_agent.run(text)

            # Creative → OpenAI
            if intent == "creative":
                return self.creative_agent.run(text)

            # Research → OpenAI → Gemini → Perplexity
            if intent == "research":
                # Step 1: OpenAI
                try:
                    return self.creative_agent.run(text)
                except:
                    pass

                # Step 2: Gemini
                try:
                    return self.logic_agent.run(text)
                except:
                    pass

                # Step 3: Perplexity fallback
                try:
                    return self.perplexity_agent.run(text)
                except:
                    return "All engines failed."

            # Final fallback
            return self.creative_agent.run(text)

        except Exception as e:
            return f"Router ERROR: {e}"
