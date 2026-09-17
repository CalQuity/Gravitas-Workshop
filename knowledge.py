"""Connect Agno Knowledge to Pinecone's hosted embedding model.

Unified with ``retrieval/``: this module remains the single Agno-facing entry
point (settings + Knowledge), while sharing env-file conventions and index
configuration with the manual retrieval pipeline.
"""

import os
from pathlib import Path

from pinecone_agno_adapter.pinecone_adapter import PineconeHostedDb
from agno.knowledge.knowledge import Knowledge
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).parent


def _resolve_env_file() -> Path | None:
    """Return the .env file to load, honouring GRAVITAS_ENV_FILE first."""
    override = os.getenv("GRAVITAS_ENV_FILE", "").strip()
    if override:
        candidate = Path(override)
        if candidate.is_file():
            return candidate
        return None
    candidate = PROJECT_ROOT / ".env"
    return candidate if candidate.is_file() else None


def load_settings(load_file: bool = True) -> dict[str, str]:
    """Load the small set of settings used by the workshop project.

    Args:
        load_file: when True (default) load ``GRAVITAS_ENV_FILE`` if set,
            else ``PROJECT_ROOT/.env``. Pass False in tests to rely purely
            on the process environment.
    """
    if load_file:
        env_file = _resolve_env_file()
        if env_file is not None:
            load_dotenv(env_file, override=False)

    required = ["OPENROUTER_API_KEY", "PINECONE_API_KEY"]
    missing = [name for name in required if not os.getenv(name, "").strip()]
    if missing:
        raise ValueError("Missing environment variables: " + ", ".join(missing))

    return {
        "openrouter_api_key": os.environ["OPENROUTER_API_KEY"],
        "openrouter_model": os.getenv("OPENROUTER_MODEL", "openrouter/free"),
        "pinecone_api_key": os.environ["PINECONE_API_KEY"],
        "pinecone_index": os.getenv("PINECONE_INDEX", "gravitas-finresearch"),
        "pinecone_namespace": os.getenv("PINECONE_NAMESPACE", "workshop"),
        "pinecone_embed_model": os.getenv("PINECONE_EMBED_MODEL", "llama-text-embed-v2"),
        "pinecone_text_field": os.getenv("PINECONE_TEXT_FIELD", "text"),
    }


def create_knowledge(
    settings: dict[str, str] | None = None,
    validate_index: bool = False,
) -> Knowledge:
    """Build the Agno Knowledge object shared by ingestion and the agent.

    Args:
        settings: optional settings dict (as returned by :func:`load_settings`).
            When None, settings are loaded from the environment so the existing
            ``create_knowledge()`` agent call keeps working.
        validate_index: when True, call ``vector_db.create()`` to validate the
            Pinecone hosted-embedding index configuration upfront.
    """
    if settings is None:
        settings = load_settings()
    vector_db = PineconeHostedDb(
        api_key=settings["pinecone_api_key"],
        index_name=settings["pinecone_index"],
        namespace=settings["pinecone_namespace"],
        embed_model=settings["pinecone_embed_model"],
        text_field=settings["pinecone_text_field"],
    )
    if validate_index:
        vector_db.create()

    return Knowledge(
        name="Gravitas Student Knowledge",
        description="PDF pages embedded by Pinecone with llama-text-embed-v2.",
        vector_db=vector_db,
        max_results=5,
    )

    

if __name__=="__main__":

    settings = load_settings()
    knowledge = create_knowledge()

    chunks = knowledge.search(query="Management guidance by CEO")

    for i in chunks:
        print("========================================")
        print()
        print()
        print(i)
        print()
        print()
        print("========================================")
        
