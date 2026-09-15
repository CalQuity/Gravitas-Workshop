# 3. Install OpenCode and connect a coding model

OpenCode is the AI coding partner used throughout the workshop. To keep every student's permissions/configuration identical, this workshop uses the **stable OpenCode 1.x line**. Do not switch major versions during the workshop.

Its provider credential is stored by OpenCode; it does **not** belong in the workshop `.env`.

## A. Install the workshop-compatible CLI

### Windows PowerShell / macOS / Linux with npm

```bash
npm install --global opencode-ai@1.18.30
```

If you already have a working OpenCode `1.x`, you may keep it. If you intentionally use OpenCode 2 for other work, do not uninstall it blindly on a managed machine; ask a facilitator before changing your setup.

## B. Verify

Open a new terminal:

```bash
opencode --version
```

Expected for this pack: `1.x` (the tested baseline is `1.18.30`). Then change into this setup folder and launch:

```bash
opencode
```

## C. Connect OpenCode Zen

Inside the OpenCode screen:

1. Enter `/connect`.
2. Choose **OpenCode Zen**.
3. Follow the browser/key flow shown by OpenCode and paste the credential into the OpenCode prompt. **Do not paste it into `.env` or chat.**
4. Enter `/models`.
5. Prefer **Muse Spark 1.3 Contributor Free** if it is currently listed and healthy; otherwise choose another model currently labelled **Free**.
6. Ask: `Reply with READY only.`

Expected: the chosen model replies `READY`.

Free-model names, limits, and temporary capacity change. The workshop does not depend on one exact free SKU. The “Contributor Free” option may permit provider use of prompts/completions for model improvement, so never give the coding assistant secrets, private personal data, or unpublished confidential material.

If a free model is temporarily unavailable, use another currently Free-labelled model rather than adding payment details just to finish pre-work.

Continue to [Workshop skills](03b-workshop-skills.md).

Official references: [OpenCode providers](https://opencode.ai/docs/providers/) and [OpenCode Zen](https://opencode.ai/docs/zen/)
