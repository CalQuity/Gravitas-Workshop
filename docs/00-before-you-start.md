# 0. Before you start

Allow **60–90 minutes**, keep the laptop plugged in, and use a stable connection. The Python AI packages can download 2–4 GB; keep at least **16 GB free**.

## Supported computers

- Windows 10 or 11, using **PowerShell**
- macOS 12 or newer, using **Terminal**
- A current 64-bit Linux distribution, using its normal terminal

Chromebooks, Android/iOS tablets, and 32-bit systems are not supported.

## Know which command block to use

- A block labelled **PowerShell** is for Windows PowerShell—not Command Prompt.
- A block labelled **Terminal** is for macOS/Linux.
- Run one block at a time. Read its output before continuing.
- Open a new terminal after installing a command; existing terminals may have an old `PATH`.

Never paste an API key into a command, chat, screenshot, issue, or coding-agent prompt. This repository stores keys only in the local `.env` file created later.

## Install Git

Git is needed to download the starter repository and protect `.env` from commits.

### Windows

Open PowerShell:

```powershell
winget install --id Git.Git -e --source winget
```

If `winget` is unavailable, use the maintained installer from [git-scm.com/install/windows](https://git-scm.com/install/windows) and keep its default options.

### macOS

Open Terminal and run:

```bash
xcode-select --install
```

If Git is already present, macOS says the command-line tools are installed. 

Homebrew users may instead run 

```bash
brew install git
```

### Linux

Use the line for your distribution:

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install git

# Fedora
sudo dnf install git

# Arch Linux
sudo pacman -S git
```

### Verify

Open a fresh terminal:

```bash
git --version
```

Expected: Git 2.30 or newer. If this works, continue to [Python 3.13 and uv](01-python-uv.md).

Official reference: [Git installation](https://git-scm.com/install/)
