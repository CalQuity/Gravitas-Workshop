# AI²: Building AI Systems with AI — Workshop

This single repo now holds both the **pre-work setup kit** and the **workshop-day starter**. (They used to be two separate folders you kept side by side; that was confusing, so everything lives here now.)

## 1. Pre-work (do this 2–3 days before the workshop)

Follow the numbered guides in `docs/`, in order, starting with `docs/00-before-you-start.md` and including **`docs/03b-workshop-skills.md`**. By the end you should have:

- Git, Python 3.13, `uv`, Node.js/npm, and the workshop-pinned OpenCode 1.x CLI;
- the workshop Python environment synced successfully;
- OpenCode connected to a currently available free coding model;
- an OpenRouter API key for LLM inferencing;
- a Pinecone API key for vector search;
- a **Langfuse account/project and API keys** for tracing;
- the **four workshop skill packages installed for OpenCode**; and
- npm access for Agent UI.

Keep provider secrets only in the local `.env` file (copy `.env.example` to `.env` in this repo root — see `docs/08-environment-variables.md`). You may also use OpenCode with the included `setting-up-gravitas-workshop` skill for guided auto-setup.

Finish pre-work with:

```bash
uv sync --frozen
uv run python scripts/check_setup.py --imports
uv run python scripts/check_langfuse.py
```

Confirm the `gravitas-prework-check` trace appears in your Langfuse project, then read `docs/09-final-check.md` for the full manual checklist.

## 2. Workshop day

From this repo run:

```bash
uv sync --frozen
uv run jupyter lab
```

Open **`notebooks/AI2_Gravitas_Workshop.ipynb`** and follow it from top to bottom. The notebook is the **main teaching + build surface**: it explains each concept in short form, reuses the key workshop diagrams where useful, asks you to predict outcomes, gives you small **YOUR TURN** stubs, and then asks you to inspect what changed. The slides support the notebook; you should not need to keep switching back to the deck to understand a concept.

The intended rhythm is **read → predict → fill a small stub → run → inspect → explain**. Most student edits are intentionally 2–8 minute tasks rather than large blank coding exercises.

### You edit four learning surfaces

- `notebooks/AI2_Gravitas_Workshop.ipynb` — cells marked **YOUR TURN** (edit these manually in Jupyter);
- `student_work/indexing.py` — preserve text + provenance in the vector record;
- `student_work/retrieval.py` — implement RRF; and
- `student_work/agent.py` — assemble the research agent.

OpenCode can explain any file, but its project permissions intentionally allow edits only in the `student_work/` files. This prevents an AI coding assistant from rewriting tests or workshop infrastructure behind your back.

### Keep Langfuse open in another tab

Langfuse is part of the classroom loop, not an end-of-day extra. At several notebook checkpoints you will **flush the current trace, open the Langfuse dashboard, and inspect the span tree** before moving on.

The four OpenCode workshop skill packages were installed during pre-work and are global, so you should not reinstall them.

## Case study

You are building an evidence-first financial-research agent over a small official corpus from **TCS, Infosys, and HCLTech**. You will observe why a plain LLM is insufficient, then add parsing, chunking, retrieval, RAG, hybrid search, reranking, tools, an agent loop, guardrails, skills, a sandbox concept, persistent runtime state, and traces.

## Troubleshooting

See `docs/troubleshooting.md` for setup issues (versions, provider errors, skills, Agent UI ports, etc.).
