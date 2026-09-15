# 5. Create a Pinecone account and API key

Pinecone is the workshop's vector database. During ingestion, filing chunks are stored as records; during retrieval, a question is embedded and matched against those records for grounded RAG answers.

Account steps are the same on Windows, macOS, and Linux.

## A. Create a free account

1. Open [app.pinecone.io](https://app.pinecone.io/) and choose **Sign up**.
2. Sign up with an available method and verify the email address if requested.
3. Once signed up, you can select **I'm building a small or personal project**. It is free and sufficient for the workshop.
4. Complete onboarding. Pinecone may create an organization and initial project automatically; if it asks for names, use `gravitas-workshop`. Do not start a paid Builder plan or Standard trial for this workshop.
5. Pinecone may give the API key upon successful completion of onboarding. You can copy that keep it. If not:
    - In the Pinecone console, select the project you will use.
    - Open **API keys**.
    - Select **Create API key**.
    - Name it `gravitas-workshop`.
    - On Starter, choose **All** if a permission selector appears; that is the available Starter permission.
    - Select **Create key**.
    - Copy the generated value immediately and keep the dialog open until it is safely in your local `.env` with variable name as PINECONE_API_KEY.

Pinecone does not show the value again after the dialog closes. Current keys may begin with `pckey_`, but do not reject an older valid key only because its prefix differs.

## C. What success looks like

The **API keys** page shows a key named `gravitas-workshop`. Put its value in `PINECONE_API_KEY` during [step 8](08-environment-variables.md). The index is expected to appear only after the Session 2 ingestion command runs.

Continue to [Langfuse](06-langfuse.md).

Official references: [Pinecone quickstart](https://docs.pinecone.io/guides/get-started/quickstart) and [manage API keys](https://docs.pinecone.io/guides/projects/manage-api-keys)
