# 7. Prepare Agno Agent UI

Agent UI is Agno's Next.js chat interface for an AgentOS backend. Node.js 24 LTS is recommended; Node.js 22 LTS also works.

## What to do during pre-work

Confirm that npm can find the current installer:

```bash
npm view create-agent-ui@latest version
```

Expected: a version number. This proves Node.js, npm, DNS, and the npm registry are reachable. Do not create the frontend yet unless the facilitators have shared the starter repository.

## Recommended setup on workshop day

From the directory where you want the frontend, run:

```bash
npx create-agent-ui@latest
```

Follow the prompts, it will help you to start your local frontend.

Open [http://localhost:3000](http://localhost:3000). Agent UI expects AgentOS at [http://localhost:7777](http://localhost:7777) by default; the endpoint can be edited in its left sidebar.

## Manual alternative

Use this only if the generator fails:

```bash
git clone https://github.com/agno-agi/agent-ui.git
cd agent-ui
corepack enable pnpm
pnpm install
pnpm dev
```

The repository's main branch currently targets Agno v2.x, which is why this setup pins `agno` below version 3. Do not run `npm install next` globally; the project already pins its compatible Next.js release.

## Expected connection states

- Browser opens but says it cannot connect: frontend works; start AgentOS on port 7777.
- Port 3000 is busy: stop the old frontend or run `pnpm exec next dev -p 3001`.
- Agent list is empty: check the AgentOS terminal for errors and confirm the endpoint shown in the sidebar.

Continue to [environment variables](08-environment-variables.md).

Official references: [Agent UI repository](https://github.com/agno-agi/agent-ui) and [AgentOS connection troubleshooting](https://docs.agno.com/faq/agentos-connection)
