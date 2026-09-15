#!/usr/bin/env python3
import argparse
import importlib.util
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPORTS = [
    "agno", "fastapi", "jupyterlab", "langfuse", "liteparse", "openai",
    "pandas", "pinecone", "pydantic", "pytest", "dotenv", "rank_bm25",
    "uvicorn", "yfinance",
]
REQUIRED_ENV = [
    "OPENROUTER_API_KEY",
    "PINECONE_API_KEY",
    "LANGFUSE_PUBLIC_KEY",
    "LANGFUSE_SECRET_KEY",
    "LANGFUSE_BASE_URL",
]


def run_version(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
        text = (p.stdout + "\n" + p.stderr).strip()
        return p.returncode == 0, text
    except Exception as exc:
        return False, str(exc)


def first_version(text):
    m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", text)
    return tuple(int(x or 0) for x in m.groups()) if m else None


def report(level, name, detail=""):
    print(f"{level:<4} {name}" + (f" — {detail}" if detail else ""))


def installed_skill_names():
    """Inspect only skill directory names; never open skill files or secrets."""
    roots = [
        Path.home() / ".agents" / "skills",
        Path.home() / ".config" / "opencode" / "skills",
    ]
    names = set()
    for root in roots:
        if not root.exists():
            continue
        for p in root.iterdir():
            if p.is_dir() or p.is_symlink():
                names.add(p.name)
    return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--imports", action="store_true")
    args = ap.parse_args()
    passed = warnings = failed = 0

    def check(ok, name, detail="", warn=False):
        nonlocal passed, warnings, failed
        if ok:
            passed += 1
            report("PASS", name, detail)
        elif warn:
            warnings += 1
            report("WARN", name, detail)
        else:
            failed += 1
            report("FAIL", name, detail)

    ok, out = run_version(["git", "--version"]) if shutil.which("git") else (False, "not found")
    v = first_version(out)
    check(bool(ok and v and v >= (2, 30, 0)), "git", out.splitlines()[0] if out else "not found")

    ok, out = run_version(["uv", "--version"]) if shutil.which("uv") else (False, "not found")
    v = first_version(out)
    check(bool(ok and v and v >= (0, 8, 0)), "uv", out.splitlines()[0] if out else "not found")

    ok, out = run_version(["node", "--version"]) if shutil.which("node") else (False, "not found")
    v = first_version(out)
    check(bool(ok and v and v[0] in (22, 24)), "node", out.splitlines()[0] if out else "need Node 22 or 24 LTS")

    ok, out = run_version(["npm", "--version"]) if shutil.which("npm") else (False, "not found")
    check(ok, "npm", out.splitlines()[0] if out else "not found")

    ok, out = run_version(["opencode", "--version"]) if shutil.which("opencode") else (False, "not found")
    v = first_version(out)
    check(bool(ok and v and v[0] == 1), "opencode", out.splitlines()[0] if out else "install workshop-pinned OpenCode 1.x")

    py_ok = (3, 13) <= sys.version_info[:2] < (3, 15)
    check(py_ok, "python", sys.version.split()[0] + " (need 3.13.x or 3.14.x)")

    gi = ROOT / ".gitignore"
    gi_ok = gi.exists() and any(line.strip() == ".env" for line in gi.read_text(errors="ignore").splitlines())
    check(gi_ok, ".gitignore", "contains .env" if gi_ok else "missing .env rule")
    if not (ROOT / ".git").exists():
        check(False, "git repository", "ZIP distributions are not Git repos; this is okay.", warn=True)

    env = ROOT / ".env"
    if not env.exists():
        check(False, ".env", "missing")
    else:
        check(True, ".env", "present")
        vals = {}
        for line in env.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, val = line.split("=", 1)
                vals[k.strip()] = val.strip()

        for key in REQUIRED_ENV:
            val = vals.get(key, "")
            configured = bool(val and not val.startswith("your-"))
            if key == "LANGFUSE_BASE_URL":
                configured = bool(val.startswith("http://") or val.startswith("https://"))
            check(configured, key, "configured (hidden)" if configured else "missing/placeholder")

        model = vals.get("OPENROUTER_MODEL", "openrouter/free")
        check(bool(model), "OPENROUTER_MODEL", model or "missing")
        check(bool(vals.get("PINECONE_INDEX", "gravitas-finresearch")), "PINECONE_INDEX", vals.get("PINECONE_INDEX", "gravitas-finresearch"))
        check(bool(vals.get("PINECONE_NAMESPACE", "workshop")), "PINECONE_NAMESPACE", vals.get("PINECONE_NAMESPACE", "workshop"))

    names = installed_skill_names()
    check("agno" in names, "skill: agno", "installed globally for OpenCode" if "agno" in names else "missing — see docs/03b-workshop-skills.md")
    check("brainstorming" in names, "skill: brainstorming", "installed globally for OpenCode" if "brainstorming" in names else "missing — see docs/03b-workshop-skills.md")
    check("langfuse" in names, "skill: langfuse", "installed globally for OpenCode" if "langfuse" in names else "missing — see docs/03b-workshop-skills.md")
    pinecone = sorted(n for n in names if n.startswith("pinecone"))
    check(bool(pinecone), "skills: pinecone", ", ".join(pinecone[:4]) if pinecone else "missing — see docs/03b-workshop-skills.md")

    if args.imports:
        for mod in IMPORTS:
            check(importlib.util.find_spec(mod) is not None, f"import {mod}")

    print(f"\nSummary: {passed} passed, {warnings} warnings, {failed} failed.")
    if failed:
        print("Workshop setup is NOT ready yet.")
        return 1
    print("Workshop setup is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
