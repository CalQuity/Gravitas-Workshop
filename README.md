# Gravitas AI² — Pre-work Setup

Complete this **2–3 days before the workshop**. This pack contains only environment preparation. The day-of Starter Kit is distributed separately.

## What “ready” means

By the end of pre-work you should have:

- Git, Python 3.13, `uv`, Node.js/npm, and the workshop-pinned OpenCode 1.x CLI;
- the workshop Python environment synced successfully;
- OpenCode connected to a currently available free coding model;
- an OpenRouter API key for the workshop LLM calls;
- a Pinecone API key for vector search;
- a **Langfuse account/project and API keys** for tracing;
- the **four workshop skill packages installed for OpenCode**; and
- npm access for Agent UI.

Langfuse is part of the **core** workshop. We will open the dashboard several times—after the plain LLM, after RAG, after the agent/tool loop, and near the final app—to inspect traces and spans while the system evolves.

## Do this in order

1. Follow the numbered guides in `docs/`, including **`03b-workshop-skills.md`**.
2. Keep provider secrets only in the local `.env` file.
3. You may use OpenCode with the included `setting-up-gravitas-workshop` skill for guided setup.
4. Finish with:

```bash
uv sync --frozen
uv run python scripts/check_setup.py --imports
```

5. Send one tiny **pre-work trace** to Langfuse as described in `docs/06-langfuse.md` and confirm it appears in your project.

## Keep this folder for workshop morning

Do **not** delete or rename the extracted `Gravitas_Prework_Setup` folder after setup. On workshop morning, put the Starter Kit **next to it**, like this:

```text
Gravitas_AI2/
├── Gravitas_Prework_Setup/
│   └── .env                 # your local secrets stay here
└── Gravitas_Workshop_Starter/
    └── notebooks/
```

The Starter Kit intentionally reuses the `.env` from this pre-work folder, so students never have to copy secrets into a second project.
