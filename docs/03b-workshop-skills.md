# 3B. Install the four workshop skills

We use **skills** to give OpenCode reusable, task-specific procedures. Install them during pre-work so workshop time is spent building rather than downloading extensions.

Install them **globally for OpenCode**. That makes the same skills available in this repo on workshop morning too.

> These commands download public repositories. Run them from a normal terminal, not from inside the Python notebook.

## 1. Pinecone skills

```bash
npx skills add pinecone-io/skills -g -a opencode -y
```

Pinecone's repository contains several skills. We will mainly use its quickstart/query patterns while building and debugging the vector-search layer.

## 2. Agno skill

```bash
npx skills add agno-agi/agno-skills --skill agno -g -a opencode -y
```

We use this when reasoning about Agno agents, tools, teams/subagents, workflows, and integrations.

## 3. Superpowers brainstorming skill

```bash
npx skills add https://github.com/obra/superpowers --skill brainstorming -g -a opencode -y
```

We use only the `brainstorming` skill in this workshop. It is an example of a reusable **process skill**: think through a design before asking the coding assistant to implement it.

> The Superpowers project also has its own OpenCode plugin installation path. For this workshop we intentionally install only the single `brainstorming` skill through the skills CLI so the class has one consistent setup flow.

## 4. Langfuse skill

```bash
npx skills add langfuse/skills --skill langfuse -g -a opencode -y
```

This lets the coding assistant use current Langfuse concepts and APIs while we add and inspect tracing.

## Verify

```bash
npx skills list -g -a opencode
```

You should be able to find:

- `agno`
- `brainstorming`
- `langfuse`
- one or more skills whose names start with `pinecone-`

Then launch OpenCode and ask its native skill tool to **list available skills**. Do not paste API keys into the OpenCode conversation.

If only one skill failed to install, rerun only that command. See `troubleshooting.md` before trying a different install method.

Continue to [OpenRouter](04-openrouter.md).
