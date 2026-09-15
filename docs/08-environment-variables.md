# 8. Create the local `.env`

The workshop Python code reads service credentials from one local `.env` file. The file must never leave your laptop.

## A. Copy the template

Run this from the `Gravitas_Prework_Setup` folder.

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### macOS/Linux Terminal

```bash
cp .env.example .env
```

Open `.env` in your normal text editor.

## B. Fill the required values

The template contains exactly:

```dotenv
OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_MODEL=openrouter/free
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX=gravitas-finresearch
PINECONE_NAMESPACE=workshop
LANGFUSE_PUBLIC_KEY=your-langfuse-public-key
LANGFUSE_SECRET_KEY=your-langfuse-secret-key
LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

Replace the OpenRouter, Pinecone, and Langfuse placeholder credentials. Keep the non-secret defaults unless a facilitator tells you otherwise.

For Langfuse, change `LANGFUSE_BASE_URL` only if your project uses a different Langfuse Cloud data region or a self-hosted instance.

Rules:

- one `NAME=value` per line;
- no spaces around `=`;
- quotes are unnecessary here;
- never put the OpenCode Zen credential in this file;
- never put real values in `.env.example`; and
- never share `.env` when asking for help.

## C. Verify the protection file

This setup may have been distributed as a ZIP rather than a Git clone, so `git check-ignore` is not always meaningful. Confirm that the included `.gitignore` contains `.env`:

```bash
cat .gitignore
```

On PowerShell:

```powershell
Get-Content .gitignore
```

If this folder happens to be inside a Git repository, you may additionally run `git check-ignore .env`.

## D. Run the safe environment check

```bash
uv run python scripts/check_setup.py
```

The checker reports whether required variables are configured but never prints their values. Fix every **FAIL**, then run the Langfuse test in `docs/06-langfuse.md` and continue to the [final check](09-final-check.md).
