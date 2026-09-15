# 2. Install Node.js LTS

Node.js and npm run the Next.js-based Agent UI. Install **Node.js 24 LTS**. Node.js 22 LTS is also accepted; Node.js 20 is EOL and should be upgraded.

## A. Check first

```bash
node --version
npm --version
```

If Node reports `v24.x` or `v22.x` and npm prints a version, keep them and continue to the verification section.

## B. Install

### Windows PowerShell

```powershell
winget install --id OpenJS.NodeJS.LTS -e
```

Alternatively, download the **LTS** Windows installer from [nodejs.org/en/download](https://nodejs.org/en/download) and keep the npm option selected.

### macOS Terminal

Use the **LTS** `.pkg` installer from [nodejs.org/en/download](https://nodejs.org/en/download), or with Homebrew:

```bash
brew install node@24
brew link --overwrite --force node@24
```

### Linux Terminal

Distribution repositories often contain an obsolete Node release. Use `nvm`, a user-scoped Node version manager:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.7/install.sh | bash
```

Open a new terminal, then run:

```bash
nvm install 24
nvm alias default 24
```

If `nvm` is not found, follow the two lines printed at the end of its installer to load it in the current shell.

## C. Verify

Open a new terminal:

```bash
node --version
npm --version
npm view create-agent-ui@latest version
```

Expected: Node `v24.x` or `v22.x`, an npm version, and an Agent UI package version. The final command checks npm access; it does not install anything globally.

Do not install `next` globally. Agent UI includes its compatible Next.js version inside its own project.

Continue to [opencode](03-opencode.md).

Official reference: [Node.js downloads and LTS status](https://nodejs.org/en/download)

