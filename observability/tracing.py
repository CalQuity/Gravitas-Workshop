"""Langfuse helpers used throughout the workshop.

The workshop deliberately keeps instrumentation small and visible:
- direct OpenAI-compatible model calls use Langfuse's OpenAI wrapper;
- selected retrieval/tool functions use @observe spans;
- notebook agent runs are wrapped in an observed parent span.

AgentOS local tracing remains enabled as a secondary local view.
"""

import os

from langfuse import get_client

from config import load_workshop_env


def langfuse_configured() -> bool:
    load_workshop_env()
    required = ("LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY", "LANGFUSE_BASE_URL")
    return all(bool(os.getenv(k)) for k in required)


def flush_langfuse() -> None:
    """Flush background trace export before students open the dashboard."""
    load_workshop_env()
    get_client().flush()


def dashboard_base_url() -> str:
    load_workshop_env()
    return os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com").rstrip("/")


if __name__ == "__main__":
    print("Langfuse configured:", langfuse_configured())
    print("Dashboard base URL:", dashboard_base_url())
