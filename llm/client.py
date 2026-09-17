import os

from langfuse import observe
from langfuse.openai import OpenAI

from config import load_workshop_env


def client():
    load_workshop_env()
    return OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )


@observe(name="workshop-llm-call")
def call_model(messages, *, model=None, temperature=0):
    load_workshop_env()
    model = model or os.getenv("OPENROUTER_MODEL", "openrouter/free")
    response = client().chat.completions.create(
        name="openrouter-chat",
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content
