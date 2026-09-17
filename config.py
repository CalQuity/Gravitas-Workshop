from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent

def find_env() -> Path:
    p = ROOT / '.env'
    if p.exists(): return p
    raise FileNotFoundError('No workshop .env found. Copy .env.example to .env in this repo root and fill it in (see docs/08-environment-variables.md).')

def load_workshop_env() -> Path:
    p = find_env(); load_dotenv(p, override=False); return p
