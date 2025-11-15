from dotenv import load_dotenv
load_dotenv()

import os
import sys

# Ensure module paths work on Kaggle, VS Code, GitHub
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from engines.openai_engine import OpenAIEngine
from engines.gemini_engine import GeminiEngine
from engines.perplexity_engine import PerplexityEngine
from core.router import Router


class USAABrain:
    """
    Orchestrator that initializes engines in safe-mode:
    - If key missing → engine disabled (no crash)
    - Router auto-selects first available engine
    - If no engines enabled → fallback safe-mode response
    """

    def __init__(self, config=None):
        all_engines = {
            "openai": OpenAIEngine(),
            "gemini": GeminiEngine(),
            "perplexity": PerplexityEngine()
        }

        # Filter out disabled engines
        self.engines = {k: v for k, v in all_engines.items() if v.enabled}

        # If no engines active → safe fallback
        if not self.engines:
            self.safe_mode = True
        else:
            self.safe_mode = False
            self.router = Router(self.engines)

    def process(self, text: str) -> str:
        if self.safe_mode:
            return f"(SAFE MODE ACTIVE — No API keys)\nMessage: {text}"

        return self.router.handle(text)
