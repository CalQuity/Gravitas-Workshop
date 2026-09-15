# 6. Set up Langfuse tracing

Langfuse is our **trace dashboard** for the workshop. We will return to it after major milestones rather than treating observability as a final add-on.

We will use the dashboard to inspect:

- an end-to-end **trace** for one run;
- model **generations**;
- retrieval/tool **spans** and their inputs/outputs;
- parent/child relationships between steps;
- latency, token usage, and errors.

The habit we want is simple:

> **When an AI system behaves strangely, inspect the execution path before changing the prompt.**

## A. Create a Langfuse Cloud project

1. Create/sign in to a Langfuse Cloud account.
2. Create a project named something like `gravitas-ai2`.
3. Open **Settings → API Keys**.
4. Create/copy the project's **public key** and **secret key**.
5. Note the data-region URL shown by your project.

Do not paste either key into chat, OpenCode, screenshots, or a shared document.

## B. Put the keys in your local `.env`

Do not edit `.env.example` with real secrets. In `docs/08-environment-variables.md` you will copy the template to `.env`.

The Langfuse entries are:

```dotenv
LANGFUSE_PUBLIC_KEY=your-langfuse-public-key
LANGFUSE_SECRET_KEY=your-langfuse-secret-key
LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

`https://cloud.langfuse.com` is the EU endpoint. If your Langfuse project is in another data region, use the base URL shown for that project.

## C. Send one safe test trace

After `.env` exists and `uv sync --frozen` has completed, run this from the setup folder:

```bash
uv run python scripts/check_langfuse.py
```

Expected terminal output:

```text
Langfuse authentication: PASS
Sent trace: gravitas-prework-check
Open your Langfuse project and confirm the trace is visible.
```

Then open **Tracing → Traces** in Langfuse and find `gravitas-prework-check`.

This is intentionally tiny. Workshop-day traces will contain generations, retrieval/tool spans, and nested agent work.

Continue to [Agent UI](07-agent-ui.md).
