"""Structured-output schema for the research agent's answers.

A schema controls format (fields, types) — it does not make the content true.
See `ResearchAnswer` for the shape every generated answer should validate against.
"""

import json

from pydantic import BaseModel, Field


class Citation(BaseModel):
    """One piece of evidence backing a claim: which source, and which page."""

    source_id: str
    page: int | None = None


class ResearchAnswer(BaseModel):
    """A model answer plus its citations and a self-reported confidence level."""

    answer: str
    citations: list[Citation] = Field(default_factory=list)
    confidence: str = Field(pattern='^(low|medium|high)$')


def parse_structured_answer(text: str) -> ResearchAnswer:
    """Validate a JSON string against ResearchAnswer, raising if it doesn't match."""
    return ResearchAnswer.model_validate(json.loads(text))


if __name__ == '__main__':
    print(parse_structured_answer('{"answer": "Revenue grew 4.2%.", "citations": [], "confidence": "medium"}'))
