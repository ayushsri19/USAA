from dotenv import load_dotenv
load_dotenv()

import os
from src.engines.openai_engine import OpenAIEngine
from src.engines.gemini_engine import GeminiEngine
from src.engines.perplexity_engine import PerplexityEngine
from src.core.router import Router

class USAABrain:
    """
    Orchestrator that initializes engines and router.
    Router expects an engines dict.
    """
    def __init__(self, config=None):
        # Initialize engines using environment variables (.env must be set)
        # Engines themselves will raise if keys missing (so you get an immediate error).
        self.engines = {
            "openai": OpenAIEngine(),
            "gemini": GeminiEngine(),
            "perplexity": PerplexityEngine()
        }
        self.router = Router(self.engines)

    def process(self, text: str) -> str:
        """Helper if you want to call brain.process(...) instead of router.handle"""
        return self.router.handle(text)