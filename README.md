# AI²: Building AI Systems with AI — Workshop

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

Open **`notebooks/01_llm_foundations.ipynb`** and work through the series in order — it's split into four notebooks so each session stays focused:

1. `01_llm_foundations.ipynb` — a plain LLM, its failure modes, temperature, structured outputs
2. `02_evidence_layer.ipynb` — provenance, parsing, chunking
3. `03_indexing_and_rag.ipynb` — vector indexing and a first RAG loop
4. `04_hybrid_retrieval.ipynb` — combining dense + keyword search

Each notebook is the **main teaching + build surface** for its section: it explains each concept in short form, reuses the key workshop diagrams where useful, asks you to predict outcomes, gives you small **YOUR TURN** stubs (numbered in order within each notebook), points to the underlying `.py` files with **📎 Script reference** notes, and then asks you to inspect what changed. The slides support the notebooks; you should not need to keep switching back to the deck to understand a concept.

The intended rhythm is **read → predict → fill a small stub → run → inspect → explain**. Most student edits are intentionally 2–8 minute tasks rather than large blank coding exercises.

### You edit these learning surfaces

Every exercise is a cell marked **YOUR TURN** inside `notebooks/01_llm_foundations.ipynb` through `04_hybrid_retrieval.ipynb` — edit these manually in Jupyter, in order. That includes Mission 7's indexing-record exercise and Mission 9's RRF exercise: write your own version in the notebook and check it against the sample data there. (The real pipeline uses its own working implementation of each — in `retrieval/ingestion/index_corpus.py` and `retrieval/search/fusion.py` — so Mission 8/9 still work end-to-end regardless of how your notebook version turns out.)

OpenCode can explain any file, but its project permissions intentionally deny edits everywhere. This prevents an AI coding assistant from writing your exercises or rewriting workshop infrastructure behind your back — you do the typing.

Tool use and a full agent loop (guardrails, skills, a sandbox concept, persistent runtime state) build on this same retrieval stack in a **separate follow-on session** — they're not part of these four notebooks.

### Keep Langfuse open in another tab

Langfuse is part of the classroom loop, not an end-of-day extra. At several notebook checkpoints you will **flush the current trace, open the Langfuse dashboard, and inspect the span tree** before moving on.

The four OpenCode workshop skill packages were installed during pre-work and are global, so you should not reinstall them.

## Case study

You are building a research agent that answers evidence-backed questions about company filings. For this workshop we limit the corpus to three companies — **TCS, Infosys, and HCLTech** — so downloading, parsing, and indexing stays fast enough to do live; the same pipeline works over any set of official filings. You will observe why a plain LLM is insufficient, then add parsing, chunking, retrieval, RAG, hybrid search, and reranking — all with full tracing. Tool use and a full agent loop (guardrails, skills, a sandbox concept, persistent runtime state) build on this same stack in a separate follow-on session.

## Troubleshooting

See `docs/troubleshooting.md` for setup issues (versions, provider errors, skills, Agent UI ports, etc.).
