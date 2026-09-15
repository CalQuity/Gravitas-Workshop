# 1. Install Python 3.13 and uv

Python runs the ingestion pipeline, RAG tools, Agno agent, and notebooks. `uv` installs Python and the workshop packages into an isolated `.venv` so other Python projects on your laptop are not changed.

## A. Check what is already installed

### Windows PowerShell

```powershell
py -3.13 --version
uv --version
```

### macOS/Linux Terminal

```bash
python3.13 --version
uv --version
```

If Python reports `3.13.x` or `3.14.x`, keep it. If `uv` prints a version, skip to **C. Create the workshop environment**.

## B. Install uv, then Python 3.13

The most consistent option on all three operating systems is Astral's standalone `uv` installer. `uv` can then install a user-scoped Python 3.13 without replacing the operating system's Python.

### Windows PowerShell

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close PowerShell, open a new one, then run:

```powershell
uv python install 3.13
uv python list 3.13
```

### macOS/Linux Terminal

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close Terminal, open a new one, then run:

```bash
uv python install 3.13
uv python list 3.13
```

If the new terminal still cannot find `uv`, run the PATH command printed by the installer, then open one more terminal.

### Prefer the Python.org installer?

That is also supported:

- Windows: install Python 3.13 from [python.org/downloads](https://www.python.org/downloads/); select **Add python.exe to PATH** and the Python launcher.
- macOS: use the **macOS 64-bit universal2 installer** from the same page.
- Linux: avoid replacing `/usr/bin/python3`. Distro repositories frequently do not carry Python 3.13; the `uv python install 3.13` method above is safer.

`uv` automatically uses an existing compatible Python, so do not install a second copy if the version check already passed.

## C. Create the workshop environment

Change into this workshop repository root, then run:

```bash
uv venv --python 3.13
uv sync --frozen
```

Expected: a local `.venv` is created and dependencies install without changing system Python. The first sync may download large ML/document-processing dependencies and can take 10–25 minutes.

Activate the environment if you want `python` to point to it directly.

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
python --version
```

### macOS/Linux Terminal

```bash
source .venv/bin/activate
python --version
```

Expected: Python 3.13.x. Activation is optional: `uv run python ...` always uses the project environment.

## D. Verify the packages

```bash
uv run python -c "import agno, pinecone, liteparse, openai; print('Python packages: OK')"
```

Expected: `Python packages: OK`. Warnings about model caches or optional GPU acceleration are fine.

Continue to [Node.js](02-nodejs.md).

Official references: [install uv](https://docs.astral.sh/uv/getting-started/installation/), [install Python with uv](https://docs.astral.sh/uv/guides/install-python/), and [Python downloads](https://www.python.org/downloads/)
