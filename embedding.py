"""Connect Agno Knowledge to Pinecone's hosted embedding model."""

from httpx2 import query
from httpx import __name

import os
from pathlib import Path

from pinecone_agno_adapter.pinecone_adapter import PineconeHostedDb
from agno.knowledge.knowledge import Knowledge
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).parent


def load_settings() -> dict[str, str]:
    """Load the small set of settings used by the workshop project."""
    
    load_dotenv(PROJECT_ROOT / ".env", override=False)

    required = ["OPENROUTER_API_KEY", "PINECONE_API_KEY"]
    missing = [name for name in required if not os.getenv(name, "").strip()]
    if missing:
        raise ValueError("Missing environment variables: " + ", ".join(missing))

    return {
        "openrouter_api_key": os.environ["OPENROUTER_API_KEY"],
        "openrouter_model": os.getenv("OPENROUTER_MODEL", "openrouter/free"),
        "pinecone_api_key": os.environ["PINECONE_API_KEY"],
        "pinecone_index": os.getenv("PINECONE_INDEX", "gravitas-finresearch"),
        "pinecone_namespace": os.getenv("PINECONE_NAMESPACE", "workshop-documents"),
        "pinecone_embed_model": os.getenv("PINECONE_EMBED_MODEL", "llama-text-embed-v2"),
        "pinecone_text_field": os.getenv("PINECONE_TEXT_FIELD", "text"),
    }


def create_knowledge() -> Knowledge:
    """Build the Agno Knowledge object shared by ingestion and the agent."""
    settings = load_settings()
    vector_db = PineconeHostedDb(
        api_key=settings["pinecone_api_key"],
        index_name=settings["pinecone_index"],
        namespace=settings["pinecone_namespace"],
        embed_model=settings["pinecone_embed_model"],
        text_field=settings["pinecone_text_field"],
    )

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
        
