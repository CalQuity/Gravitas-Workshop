---
name: setting-up-gravitas-workshop
description: Use when a student asks to install, prepare, verify, or troubleshoot the local development environment for the Gravitas AI² workshop on Windows, macOS, or Linux.
metadata:
  audience: university students
  project: Gravitas AI2 workshop
---

# Setting Up Gravitas Workshop

## Outcome

Prepare the supported local toolchain, all four workshop skills, and provider credentials while keeping secrets outside the agent's context. Read and follow the repository guides; do not substitute remembered commands.

## Safety contract

- Never open, read, print, source, paste, transmit, or commit `.env` values.
- Never ask the student to send an API key in chat. If a key was shared, advise immediate rotation.
- Account signup, API-key creation, payment, and secret entry are student actions in the browser.
- Do not add funds, trials, billing details, or auto-reload.
- Install Python packages only in the setup root's `.venv`; never use `pip`/`uv pip` with `--system` or `sudo`.
- Preserve installed tools that meet the required versions. Do not upgrade unrelated software.

## Workflow

1. Locate the setup root: the directory containing `pyproject.toml`, `.env.example`, `docs/`, and `scripts/check_setup.py`. Stop if these are not together.
2. Detect the operating system and shell. Read `docs/00-before-you-start.md`, then only the platform sections relevant to that system.
3. Confirm `.gitignore` contains `.env`. Do not assume a ZIP extraction is a Git repository.
4. Check versions before installing: Git 2.30+, Python 3.13+, `uv` 0.8+, Node.js 24 or 22 LTS, npm, and OpenCode 1.x.
5. Follow the tool/setup guides in order:
   - `docs/01-python-uv.md`
   - `docs/02-nodejs.md`
   - `docs/03-opencode.md`
   - `docs/03b-workshop-skills.md`
   - `docs/04-openrouter.md`
   - `docs/05-pinecone.md`
   - `docs/06-langfuse.md`
   - `docs/07-agent-ui.md`
   - `docs/08-environment-variables.md`
6. In the setup root, run `uv venv --python 3.13` only if `.venv` is absent or uses the wrong Python. Run `uv sync --frozen`.
7. If `.env` is absent, copy `.env.example` to `.env` without reading either file into chat. The student enters OpenRouter, Pinecone, and Langfuse values locally.
8. Run `uv run python scripts/check_setup.py --imports`. The checker only verifies presence/configuration; it hides all secret values.
9. Run `uv run python scripts/check_langfuse.py`. Ask the student to visually confirm the `gravitas-prework-check` trace in their Langfuse project.
10. Resolve failures using `docs/troubleshooting.md` and rerun only the failed check. Declare readiness only when the setup checker has zero failures and the Langfuse trace is visible.

## Quick reference

| Check | Required result | Repair source |
|---|---|---|
| Python | 3.13+ in `.venv` | `docs/01-python-uv.md` |
| Node.js | 24 or 22 LTS | `docs/02-nodejs.md` |
| OpenCode | 1.x and Zen connected | `docs/03-opencode.md` |
| Workshop skills | Pinecone + Agno + brainstorming + Langfuse | `docs/03b-workshop-skills.md` |
| Provider variables | OpenRouter + Pinecone + Langfuse configured; values hidden | `docs/04-openrouter.md`, `docs/05-pinecone.md`, `docs/06-langfuse.md` |
| Python imports | all PASS | `uv sync --frozen` |
| Langfuse trace | `gravitas-prework-check` visible | `docs/06-langfuse.md` |
| Agent UI package | npm can resolve it | `docs/07-agent-ui.md` |

## Common mistakes

- A missing API key is not a missing Python package; treat environment and import failures separately.
- The Zen key belongs in OpenCode's `/connect` flow, not `.env`.
- Installing a skill does not authenticate the provider it describes.
- A tool version passing does not prove packages, skills, or provider variables are ready.
- A `WARN` may be acceptable; any `FAIL` means setup is not complete.
