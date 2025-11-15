import logging
logging.disable(logging.CRITICAL)

import os
import sys

# Ensure project root is on sys.path when running from src
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.orchestrator.usaa_brain import USAABrain

def run_usaa():
    brain = USAABrain()
    router = brain.router

    try:
        print("Ask USAA anything: ", end="", flush=True)
        while True:
            text = input()
            if not text.strip():
                print("Ask USAA anything: ", end="", flush=True)
                continue

            # send to router
            result = router.handle(text)

            print(result)
            print("Ask USAA anything: ", end="", flush=True)

    except KeyboardInterrupt:
        print("\nUSAA stopped. Goodbye.")

if __name__ == "__main__":
    run_usaa()