# 9. Final workshop-readiness check

Run this from the repo root after completing every guide:

```bash
uv run python scripts/check_setup.py --imports
```

The checker is local and non-mutating. It does not print credential values.

Then run:

```bash
uv run python scripts/check_langfuse.py
```

Open your Langfuse project and confirm the `gravitas-prework-check` trace appears.

## Read the result

- **PASS**: ready.
- **WARN**: not blocking, but read the message.
- **FAIL**: fix before the workshop.

A ready setup checker ends with `Workshop setup is ready.`

## Manual checklist

- [ ] Git 2.30+ works.
- [ ] Python 3.13.x or 3.14.x runs inside `.venv`.
- [ ] `uv sync --frozen` finishes and required imports pass.
- [ ] Node.js 24 LTS or 22 LTS and npm work.
- [ ] npm can find `create-agent-ui@latest`.
- [ ] OpenCode 1.x launches with the workshop-compatible config.
- [ ] `/connect` has a working OpenCode Zen credential.
- [ ] `/models` has a currently available Free-labelled model.
- [ ] The four workshop skill packages are installed for OpenCode.
- [ ] OpenRouter, Pinecone, and Langfuse credentials are in `.env`.
- [ ] `gravitas-prework-check` is visible in the Langfuse dashboard.
- [ ] `.gitignore` contains `.env`.

## Workshop day

Pre-work and the workshop-day notebook live in this same repo, so there is nothing else to fetch or extract. From the repo root, run:

```bash
uv sync --frozen
uv run jupyter lab
```

Then open `notebooks/AI2_Gravitas_Workshop.ipynb`. It automatically finds the `.env` you created here during pre-work.

## If anything fails

Open [troubleshooting.md](troubleshooting.md), find the exact symptom, and try only that fix. If it still fails, send facilitators:

1. operating system and version;
2. failing check name;
3. exact command;
4. complete error text; and
5. what you already tried.

Hide API keys, email addresses, usernames, and private file paths in screenshots.

Do not create paid resources just to pass setup unless facilitators explicitly ask.
