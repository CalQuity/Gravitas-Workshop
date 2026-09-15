# 4. Create an OpenRouter account and API key

OpenRouter provides the OpenAI-compatible runtime used by the starter application. The core workshop uses text-readable PDFs; scanned-PDF OCR is deliberately outside the beginner path.

Account steps are the same on Windows, macOS, and Linux.

## A. Create the account

1. Open the provided link: [OpenRouter sign in → Default workspace keys](https://openrouter.ai/sign-in?redirect_url=%2Fworkspaces%2Fdefault%2Fkeys).
2. Sign in with an available method such as Google, GitHub, or email.
3. Confirm that the workspace picker shows **Default**. A personal workshop does not need a new organization or workspace.

## B. Create the key

1. Open **Keys** in the Default workspace. The direct page is [openrouter.ai/keys](https://openrouter.ai/keys).
2. Select **Create API Key**.
3. Name it `gravitas-workshop`.
4. Leave the optional credit limit unset. The workshop uses free routes and does not require adding payment details.
5. Create the key and copy it immediately.

Do not paste the key into this document, opencode chat, a screenshot, or source code. Keep it temporarily in a trusted password manager or paste it directly into the local `.env` as `OPENROUTER_API_KEY` (see [step 8](08-environment-variables.md)).

## C. Understand the free tier

- `openrouter/free` automatically chooses an available free model compatible with a request.
- A model slug ending in `:free` targets that model's free variant (for example: nvidia/nemotron-3.5-lightning:free).
- Accounts without at least $10 of purchased credits are currently limited to **50 free-model requests per day in total**. Free capacity can also be busy or temporarily unavailable.
- No payment is required for the planned workshop path. Free routes are rate-limited, so avoid repeatedly rerunning model cells without a reason.

Model lists change often, which is why `.env.example` uses `OPENROUTER_MODEL=openrouter/free` instead of a stale model slug.

## D. What success looks like

You should now have one `gravitas-workshop` key listed under **Default workspace → Keys**. Do not try to reveal it again. The offline checker later verifies that a non-placeholder value is present without displaying it; the workshop's first model request is the online test.

Continue to [Pinecone](05-pinecone.md).

Official references: [OpenRouter quickstart](https://openrouter.ai/docs/quickstart), [authentication](https://openrouter.ai/docs/api-reference/authentication), and [free-model limits](https://openrouter.ai/docs/faq)
