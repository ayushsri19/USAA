import os
import sys
import traceback
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.orchestrator.usaa_brain import USAABrain


tests = [
    ("Creative: greeting", "hi"),
    ("Creative: beautiful question", "tell me something beautiful"),
    ("Date test", "aaj ki date?"),
    ("Day test", "aaj ka day kya hai?"),
    ("Time test", "time kya hua hai?"),
    ("Research factual", "who is Virat Kohli"),
    ("Research concept", "what is quantum entanglement"),
    ("Logic math", "solve 12 * (5 + 3)"),
    ("Logic reasoning", "why is sky blue"),
    ("Terminal ignore (activate)", "& D:\\USAA\\venv\\Scripts\\Activate.ps1"),
    ("Terminal ignore (pip)", "pip install hello"),
    ("Hallucination trap", "tell me history of aliens on Mars"),
]


def run_test(router, label, query):
    print(f"\n=== TEST: {label} ===")
    print(f"User → {query}")

    try:
        result = router.handle(query)
        print(f"USAA → {result}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        traceback.print_exc()


def main():
    print("===========================================")
    print("           USAA DIAGNOSTIC MODE")
    print("===========================================\n")

    try:
        brain = USAABrain()
        router = brain.router
    except Exception as e:
        print("\n❌ FATAL: Brain initialization failed")
        print(e)
        traceback.print_exc()
        return

    print("🚀 Running capability tests...\n")

    for label, query in tests:
        run_test(router, label, query)

    print("\n===========================================")
    print("         DIAGNOSTIC COMPLETE")
    print("Finished:", datetime.now().strftime("%d %B %Y %I:%M:%S %p"))
    print("===========================================\n")


if __name__ == "__main__":
    main()
