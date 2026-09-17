import pytest

import knowledge


def test_load_settings_reports_missing_keys(monkeypatch) -> None:
    for name in ("OPENROUTER_API_KEY", "PINECONE_API_KEY"):
        monkeypatch.delenv(name, raising=False)

    with pytest.raises(ValueError, match="OPENROUTER_API_KEY.*PINECONE_API_KEY"):
        knowledge.load_settings(load_file=False)


def test_load_settings_can_use_a_shared_env_file(monkeypatch, tmp_path) -> None:
    env_file = tmp_path / "shared.env"
    env_file.write_text(
        "OPENROUTER_API_KEY=openrouter-shared\n"
        "PINECONE_API_KEY=pinecone-shared\n"
        "PINECONE_INDEX=gravitas-finresearch\n"
    )
    monkeypatch.setenv("GRAVITAS_ENV_FILE", str(env_file))
    for name in ("OPENROUTER_API_KEY", "PINECONE_API_KEY", "PINECONE_INDEX"):
        monkeypatch.delenv(name, raising=False)

    settings = knowledge.load_settings()

    assert settings["openrouter_api_key"] == "openrouter-shared"
    assert settings["pinecone_index"] == "gravitas-finresearch"
    assert settings["pinecone_embed_model"] == "llama-text-embed-v2"


def test_create_knowledge_uses_pinecone_hosted_embeddings(monkeypatch) -> None:
    captured = {}

    class FakePineconeHostedDb:
        def __init__(self, **kwargs):
            captured.update(kwargs)

        def create(self):
            captured["validated"] = True

        def exists(self):
            return True

    monkeypatch.setattr(knowledge, "PineconeHostedDb", FakePineconeHostedDb)
    knowledge_obj = knowledge.create_knowledge(
        {
            "openrouter_api_key": "openrouter-test",
            "openrouter_model": "openrouter/free",
            "pinecone_api_key": "pinecone-test",
            "pinecone_index": "gravitas-finresearch",
            "pinecone_namespace": "tests",
            "pinecone_embed_model": "llama-text-embed-v2",
            "pinecone_text_field": "text",
        },
        validate_index=True,
    )

    assert knowledge_obj.vector_db is not None
    assert captured == {
        "api_key": "pinecone-test",
        "index_name": "gravitas-finresearch",
        "namespace": "tests",
        "embed_model": "llama-text-embed-v2",
        "text_field": "text",
        "validated": True,
    }
