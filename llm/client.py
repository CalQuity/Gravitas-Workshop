"""The plain-LLM call path: build a prompt, send it, get text back.

`build_messages` shapes a question (plus optional evidence) into the chat messages
`call_model` sends to OpenRouter. Everything here is a normal, uninstrumented-looking
call — `@observe` is what reports each one to Langfuse.
"""

import os

from langfuse import observe
from langfuse.openai import OpenAI

from config import load_workshop_env


def client():
    """An OpenRouter-backed OpenAI client, credentials loaded from .env."""
    load_workshop_env()
    return OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )


def build_messages(question: str, context: str | None = None):
    """Shape a question (and optional retrieved evidence) into chat messages."""
    system = 'You are a careful financial research assistant. Do not invent facts. If evidence is provided, use only that evidence and cite source IDs.'
    if context:
        system += '\n\nEVIDENCE:\n' + context
    return [{'role': 'system', 'content': system}, {'role': 'user', 'content': question}]


@observe(name="workshop-llm-call")
def call_model(messages, *, model=None, temperature=0.3, response_format=None):
    """Send chat messages to the configured OpenRouter model and return its text.

    Pass response_format={'type': 'json_object'} to ask the model for JSON — this
    plain JSON mode is far more widely supported across free/routed models than
    strict `json_schema` mode, so it's what this workshop uses for structured output.
    """
    load_workshop_env()
    model = model or os.getenv("OPENROUTER_MODEL", "openrouter/free")
    kwargs = {"response_format": response_format} if response_format else {}
    response = client().chat.completions.create(
        name="openrouter-chat",
        model=model,
        messages=messages,
        temperature=temperature,
        **kwargs,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    load_workshop_env()
    messages = build_messages("What was TCS FY26 revenue?")
    print(messages)
    try:
        print(call_model(messages))
    except Exception as exc:
        print(f"call_model needs OPENROUTER_API_KEY configured in .env ({exc}).")
