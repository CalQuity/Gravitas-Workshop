"""Parse one PDF into simple page dictionaries with LiteParse."""

import asyncio
from pathlib import Path

from liteparse import LiteParse


def _parse_pdf_sync(path: Path) -> list[dict[str, object]]:
    """LiteParse is synchronous, so this small function runs in a worker thread."""
    parser = LiteParse(output_format="markdown", quiet=True)
    try:
        result = parser.parse(path)
    finally:
        parser.close()

    pages = []
    for page in result.pages:
        text = (page.markdown or page.text or "").strip()
        if text:
            pages.append(
                {
                    "page": int(page.page_num),
                    "text": text,
                    "source_file": path.name,
                }
            )

    if not pages:
        raise ValueError(f"No readable text found in {path.name}")
    return pages


async def parse_pdf(path: str | Path) -> list[dict[str, object]]:
    """Parse a PDF without blocking the async ingestion loop."""
    pdf_path = Path(path)
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported")
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)
    return await asyncio.to_thread(_parse_pdf_sync, pdf_path)

