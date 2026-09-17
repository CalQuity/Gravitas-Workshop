"""Parse PDFs, add their pages to Agno Knowledge, then archive them."""

import asyncio
import json
from pathlib import Path

from agno.knowledge.reader.text_reader import TextReader

from embedding import PROJECT_ROOT, create_knowledge
from parsing import parse_pdf


def _next_destination(folder: Path, filename: str) -> Path:
    """Avoid overwriting an older file with the same name."""
    destination = folder / filename
    number = 2
    while destination.exists():
        source = Path(filename)
        destination = folder / f"{source.stem}-{number}{source.suffix}"
        number += 1
    return destination


async def ingest_documents(
    documents_dir: str | Path = PROJECT_ROOT / "documents",
    ingested_dir: str | Path = PROJECT_ROOT / "ingested",
) -> dict[str, list[str]]:
    """Ingest every PDF and move only fully successful files."""
    documents_dir = Path(documents_dir)
    ingested_dir = Path(ingested_dir)
    documents_dir.mkdir(parents=True, exist_ok=True)
    ingested_dir.mkdir(parents=True, exist_ok=True)

    knowledge = create_knowledge()
    result = {"ingested": [], "failed": [], "skipped": []}

    for pdf in sorted(documents_dir.iterdir(), key=lambda path: path.name.lower()):
        if not pdf.is_file() or pdf.name.startswith("."):
            continue
        if pdf.suffix.lower() != ".pdf":
            result["skipped"].append(pdf.name)
            continue

        try:
            pages = await parse_pdf(pdf)

            for page in pages:
                await knowledge.ainsert(
                    name=f"{pdf.name} - page {page['page']}",
                    text_content=page["text"],
                    metadata={
                        "source_file": pdf.name,
                        "page": page["page"],
                        "page_kind": "pdf_physical_1_based",
                    },
                    reader=TextReader(chunk=True, chunk_size=3000),
                    upsert=True,
                )

            destination = _next_destination(ingested_dir, pdf.name)
            await asyncio.to_thread(pdf.rename, destination)
            result["ingested"].append(destination.name)
        except Exception:
            result["failed"].append(pdf.name)

    return result


if __name__ == "__main__":
    summary = asyncio.run(ingest_documents())
    print(json.dumps(summary, indent=2))
    if summary["failed"]:
        raise SystemExit(1)
