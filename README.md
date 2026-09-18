# AI²: Building AI Systems with AI — Workshop

Slide Deck (Part 1): https://docs.google.com/presentation/d/1SJdJUETUOrCCDTdO0eA52aVkAKLf67bs/edit?usp=sharing&ouid=112409108839436100183&rtpof=true&sd=true
Slide Deck (Part 2): https://docs.google.com/presentation/d/16g3we6rBWkatHswdykJFu5_K1rDZ5KhWi5mzWoU4X0k/edit?usp=sharing

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

Open **`notebooks/01_llm_foundations.ipynb`** and work through the series in order — notebooks `01–04` cover retrieval, `05–11` build the agent on top of it:

1. `01_llm_foundations.ipynb` — a plain LLM, its failure modes, temperature, structured outputs
2. `02_evidence_layer.ipynb` — provenance, parsing, chunking
3. `03_indexing_and_rag.ipynb` — vector indexing and a first RAG loop
4. `04_hybrid_retrieval.ipynb` — combining dense + keyword search
5. `05_vanilla_agent.ipynb` — minimal Agno agent
6. `06_instructions.ipynb` — agent instructions
7. `07_knowledge.ipynb` — Agno Knowledge over the Pinecone index
8. `08_sessions.ipynb` — session/history state
9. `09_tools.ipynb` — web search, market data, calculations
10. `10_guardrails.ipynb` — PII + prompt-injection guardrails
11. `11_full_agent.ipynb` — the complete research agent (`agent.py`)

Each notebook is the **main teaching + build surface** for its section: it explains each concept in short form, reuses the key workshop diagrams where useful, asks you to predict outcomes, gives you small **YOUR TURN** stubs (numbered in order within each notebook), points to the underlying `.py` files with **📎 Script reference** notes, and then asks you to inspect what changed. The slides support the notebooks; you should not need to keep switching back to the deck to understand a concept.

The intended rhythm is **read → predict → fill a small stub → run → inspect → explain**. Most student edits are intentionally 2–8 minute tasks rather than large blank coding exercises.

### You edit these learning surfaces

Every exercise is a cell marked **YOUR TURN** inside `notebooks/01_llm_foundations.ipynb` through `04_hybrid_retrieval.ipynb` — edit these manually in Jupyter, in order. That includes Mission 7's indexing-record exercise and Mission 9's RRF exercise: write your own version in the notebook and check it against the sample data there. (The real pipeline uses its own working implementation of each — in `retrieval/ingestion/index_corpus.py` and `retrieval/search/fusion.py` — so Mission 8/9 still work end-to-end regardless of how your notebook version turns out.)

OpenCode can explain any file, but its project permissions intentionally deny edits everywhere. This prevents an AI coding assistant from writing your exercises or rewriting workshop infrastructure behind your back — you do the typing.

Tool use and the full agent loop (guardrails, skills, a sandbox concept, persistent runtime state) build on this same retrieval stack in notebooks `05–11` and `agent.py`.

### Keep Langfuse open in another tab

Langfuse is part of the classroom loop, not an end-of-day extra. At several notebook checkpoints you will **flush the current trace, open the Langfuse dashboard, and inspect the span tree** before moving on.

The four OpenCode workshop skill packages were installed during pre-work and are global, so you should not reinstall them.

## Repo layout

- `retrieval/` — the manual retrieval stack: `ingestion/` (`parsing.py`, `chunking.py`, `corpus.py`, `index_corpus.py`) and `search/` (`search.py`, `fusion.py`, `ranking.py`, `rag.py`).
- `agent_utils/` — the Agno agent-side package: `knowledge.py` (settings + `Knowledge` over Pinecone hosted `llama-text-embed-v2`), `tools.py` (web/market tools), `subagent.py` (technicals subagent).
- `agent.py` — the full research agent (`search_knowledge=True`) served via AgentOS.
- `data/` — `corpus_manifest.json` (5 official PDFs, staged S3 URLs), `documents/` (downloaded PDFs), `processed/chunks.jsonl` (built corpus).
- `notebooks/01–04` teach retrieval; `notebooks/05–11` teach the agent track.
- `tests/test_knowledge.py` covers settings + Knowledge creation.

## Ingestion state

The corpus is already ingested: 5 PDFs → `data/processed/chunks.jsonl` (1657 chunks, `RecursiveChunking` 1200/120) → Pinecone index `gravitas-finresearch`, namespace `workshop` (pinned via `PINECONE_NAMESPACE=workshop` in `.env`; both the manual path and `agent_utils.knowledge` default to it). To rebuild from scratch:

```bash
uv run python scripts/fetch_documents.py            # download data/documents/
uv run python -c "from retrieval.ingestion.corpus import build_corpus; build_corpus()"
uv run python -m retrieval.ingestion.index_corpus   # creates the index if missing
```

If Pinecone returns 429 (250k tokens/min hosted-embedding limit), re-run the upload in smaller batches with sleeps between them — record `_id`s are deterministic, so re-upserts are idempotent. `rank-bm25` is a required dependency (notebook `04` keyword search).

## Case study

You are building a research agent that answers evidence-backed questions about company filings. For this workshop we limit the corpus to three companies — **TCS, Infosys, and HCLTech** — so downloading, parsing, and indexing stays fast enough to do live; the same pipeline works over any set of official filings. You will observe why a plain LLM is insufficient, then add parsing, chunking, retrieval, RAG, hybrid search, and reranking — all with full tracing. Tool use and a full agent loop (guardrails, skills, a sandbox concept, persistent runtime state) build on this same retrieval stack in notebooks `05–11` and `agent.py` — the agent-side modules live in the `agent_utils/` package (`knowledge.py`, `tools.py`, `subagent.py`), so notebooks and `agent.py` import them as `from agent_utils.knowledge import ...`.

## Troubleshooting

See `docs/troubleshooting.md` for setup issues (versions, provider errors, skills, Agent UI ports, etc.).
