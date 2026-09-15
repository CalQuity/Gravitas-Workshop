# Troubleshooting

Find the exact symptom. Run fixes in the same shell named by the guide, then rerun the failed verification command.

## Command not found after installation

Close every terminal and open a new one. Then locate the command:

```powershell
# Windows PowerShell
Get-Command uv, python, node, npm, opencode, git -ErrorAction SilentlyContinue
```

```bash
# macOS/Linux
command -v uv python3.13 node npm opencode git
```

If the installer printed a PATH instruction, apply that exact instruction. Do not download a similarly named package from an unofficial site.

## PowerShell cannot run `Activate.ps1`

Activation is optional. Use `uv run python ...` instead. To allow activation for only the current PowerShell window:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Do not change the machine-wide policy on a managed laptop.

## Wrong Python version

List what `uv` can see:

```bash
uv python list 3.13
uv run --python 3.13 python --version
```

If missing:

```bash
uv self update
uv python install 3.13
uv venv --clear --python 3.13
uv sync
```

`uv venv --clear` replaces only this repository's `.venv`; it does not remove system Python.

## Python package installation is slow or runs out of disk

Some document/ML dependencies are large. Keep 8 GB free, plug in the laptop, and allow 10–25 minutes on the first install. Retry:

```bash
uv sync
```

`uv` reuses completed downloads. If a package says no compatible wheel exists, confirm that the interpreter is standard 64-bit CPython 3.13—not a 32-bit or free-threaded (`3.13t`) build.

## `No module named ...`

The wrong interpreter is active or dependencies were not synced:

```bash
uv sync
uv run python -c "import agno, pinecone, langfuse; print('imports OK')"
```

## Node is old even after installing LTS

Open a new terminal and inspect locations:

```powershell
# Windows
Get-Command node -All
```

```bash
# macOS/Linux
which -a node
```

Remove obsolete PATH entries through the tool that installed them. On Linux with `nvm`, run `nvm use 24 && nvm alias default 24`. Do not use `sudo npm install --global node`.

## npm permission error

Do not rerun npm with `sudo`. opencode's macOS/Linux installer does not require npm. For Agent UI, use a user-scoped Node installation from `nvm`; on Windows, reinstall Node.js LTS for the current user.

## opencode command not found

Open a fresh terminal and rerun the platform's install command from [03-opencode.md](03-opencode.md). On Windows:

```powershell
npm config get prefix
npm install --global opencode-ai@1.18.30
```

The npm prefix directory must be on PATH. Do not install the package named only `opencode`.

## Zen connection or model fails

1. Run opencode and enter `/connect` again.
2. Choose **OpenCode Zen**, not a similarly named provider.
3. Create a new Zen key only if the old credential was revoked.
4. Enter `/models` and choose a model currently labelled **Free**.
5. If free capacity is unavailable, try another Free-labelled model.

Do not paste the key into chat. If one Free-labelled model is unavailable, try another before changing any billing settings.

## Provider returns 401 or 403

The key is missing, copied incompletely, revoked, or belongs to another project. Reopen the relevant provider console, create a replacement if necessary, and update only `.env`. The checker intentionally does not display or transmit the value.

## Provider returns 429

The key is valid but has reached a rate limit or the free route is busy. Wait a few minutes and retry. For OpenRouter, try `openrouter/free`; for workshop ingestion, `LiteParse v2` continues handling normal text pages. Do not add payment to work around a temporary classroom limit without organizer direction.

## Pinecone index configuration error

Do not create a dimensioned index manually. Delete nothing during setup. Confirm:

```dotenv
PINECONE_INDEX=gravitas-finresearch
PINECONE_NAMESPACE=workshop
```

If an index with the same name but a different configuration already exists, change `PINECONE_INDEX` to a new lowercase name such as `gravitas-finresearch-2` and rerun ingestion on workshop day.

## Langfuse trace does not appear

First run the dedicated check:

```bash
uv run python scripts/check_langfuse.py
```

If authentication fails:

1. confirm `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` belong to the **same project**;
2. confirm `LANGFUSE_BASE_URL` matches that project's data region;
3. create a new API key pair if the old pair was revoked; and
4. update only your local `.env`.

If authentication passes but a trace is not visible immediately, refresh **Tracing → Traces** and make sure you are viewing the same project.

## A workshop skill is missing

Run:

```bash
npx skills list -g -a opencode
```

If `agno`, `brainstorming`, `langfuse`, or the Pinecone skills are missing, return to `docs/03b-workshop-skills.md` and rerun **only the missing install command**. Do not paste provider API keys into a skill-install command.


## Port 3000 or 7777 is busy

Stop the old process if it is yours. Otherwise run Agent UI on another port:

```bash
pnpm exec next dev -p 3001
```

Port 7777 belongs to AgentOS; change the Agent UI endpoint in the left sidebar if the workshop backend uses another port.

## `.env` appears in Git status

Do not commit. Confirm that the `.gitignore` beside `.env.example` includes `.env`. If `.env` was already tracked, untrack it without deleting the local file:

```bash
git rm --cached .env
git status --short
```

If a real key was ever committed or pushed, treat it as exposed: revoke it in the provider console and create a new key. Removing the file from the latest commit does not make the old key safe.
