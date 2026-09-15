# Gravitas AI²: Setup

Complete this **2–3 days before the workshop**.

## What “ready” means

By the end of this setup you should have:

- Git, Python 3.13, `uv`, Node.js/npm, and the workshop-pinned OpenCode 1.x CLI;
- the workshop Python environment synced successfully;
- OpenCode connected to a currently available free coding model;
- an OpenRouter API key for LLM inferencing;
- a Pinecone API key for vector search;
- a **Langfuse account/project and API keys** for tracing;
- the **four workshop skill packages installed for OpenCode**; and
- npm access for Agent UI.

## Do this in order

1. Follow the numbered guides in `docs/`, including **`03b-workshop-skills.md`**.
2. Keep provider secrets only in the local `.env` file.
3. Alternatively, you may use OpenCode with the included `setting-up-gravitas-workshop` skill for guided auto-setup.
4. Finish with:

```bash
uv sync --frozen
uv run python scripts/check_setup.py --imports
```

5. Send one tiny **pre-work trace** to Langfuse as described in `docs/06-langfuse.md` and confirm it appears in your project.
