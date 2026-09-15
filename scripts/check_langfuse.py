#!/usr/bin/env python3
"""Send one tiny pre-work trace without printing any secret values."""

from pathlib import Path

from dotenv import load_dotenv
from langfuse import get_client, observe

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env", override=False)


@observe(name="gravitas-prework-check")
def setup_check():
    return {"status": "ready", "purpose": "Gravitas AI2 setup verification"}


def main():
    client = get_client()
    if not client.auth_check():
        print("Langfuse authentication: FAIL")
        return 1

    print("Langfuse authentication: PASS")
    setup_check()
    client.flush()
    print("Sent trace: gravitas-prework-check")
    print("Open your Langfuse project and confirm the trace is visible.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
