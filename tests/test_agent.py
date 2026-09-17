from __future__ import annotations

import agent


class FakeKnowledge:
    pass


SETTINGS = {
    "openrouter_api_key": "openrouter-test",
    "openrouter_model": "openrouter/free",
    "pinecone_api_key": "pinecone-test",
    "pinecone_index": "student-test",
    "pinecone_namespace": "tests",
    "pinecone_embed_model": "llama-text-embed-v2",
    "pinecone_text_field": "text",
}


def test_create_agent_combines_knowledge_sessions_tools_and_guardrails() -> None:
    knowledge = FakeKnowledge()

    research_agent = agent.create_agent(settings=SETTINGS, knowledge=knowledge)

    names = {getattr(tool, "name", getattr(tool, "__name__", "")) for tool in research_agent.tools}
    assert research_agent.knowledge is knowledge
    assert research_agent.search_knowledge is True
    assert {"websearch", "market_ohlcv", "calculate_growth"} <= names
    assert research_agent.add_history_to_context is True
    assert len(research_agent.pre_hooks) == 2


def test_create_agent_os_exposes_agent_runs() -> None:
    research_agent = agent.create_agent(settings=SETTINGS, knowledge=FakeKnowledge())

    app = agent.create_agent_os(research_agent).get_app()

    assert "/agents/{agent_id}/runs" in app.openapi()["paths"]


def test_financial_questions_prioritize_the_knowledge_base() -> None:
    research_agent = agent.create_agent(settings=SETTINGS, knowledge=FakeKnowledge())
    instructions = " ".join(research_agent.instructions).lower()

    assert "search the knowledge base first" in instructions
    assert "latest period available in the knowledge base" in instructions
    assert "do not use web search when the knowledge base answers the question" in instructions
