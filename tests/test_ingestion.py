from __future__ import annotations

import asyncio
from pathlib import Path

import ingestion


class FakeKnowledge:
    def __init__(self):
        self.inserted = []

    async def ainsert(self, **kwargs):
        self.inserted.append(kwargs)


def test_ingestion_inserts_pages_then_moves_the_pdf(monkeypatch, tmp_path: Path) -> None:
    documents = tmp_path / "documents"
    ingested = tmp_path / "ingested"
    documents.mkdir()
    pdf = documents / "report.pdf"
    pdf.write_bytes(b"%PDF-fake")
    knowledge = FakeKnowledge()

    async def fake_parse(path):
        assert path == pdf
        return [
            {"page": 1, "text": "Page one", "source_file": "report.pdf"},
            {"page": 2, "text": "Page two", "source_file": "report.pdf"},
        ]

    monkeypatch.setattr(ingestion, "parse_pdf", fake_parse)
    result = asyncio.run(ingestion.ingest_documents(documents, ingested, knowledge=knowledge))

    assert result == {"ingested": ["report.pdf"], "failed": [], "skipped": []}
    assert not pdf.exists()
    assert (ingested / "report.pdf").exists()
    assert [item["metadata"]["page"] for item in knowledge.inserted] == [1, 2]
    assert all(item["upsert"] is True for item in knowledge.inserted)


def test_ingestion_keeps_a_pdf_when_parsing_fails(monkeypatch, tmp_path: Path) -> None:
    documents = tmp_path / "documents"
    ingested = tmp_path / "ingested"
    documents.mkdir()
    pdf = documents / "broken.pdf"
    pdf.write_bytes(b"%PDF-fake")

    async def broken_parse(path):
        raise ValueError("No readable text")

    monkeypatch.setattr(ingestion, "parse_pdf", broken_parse)

    result = asyncio.run(ingestion.ingest_documents(documents, ingested, knowledge=FakeKnowledge()))

    assert result == {"ingested": [], "failed": ["broken.pdf"], "skipped": []}
    assert pdf.exists()


def test_ingestion_skips_non_pdf_files(tmp_path: Path) -> None:
    documents = tmp_path / "documents"
    ingested = tmp_path / "ingested"
    documents.mkdir()
    (documents / "notes.txt").write_text("not a PDF")

    result = asyncio.run(ingestion.ingest_documents(documents, ingested, knowledge=FakeKnowledge()))

    assert result == {"ingested": [], "failed": [], "skipped": ["notes.txt"]}


def test_student_kit_includes_the_hcltech_sample_pdf() -> None:
    project_root = Path(__file__).parents[1]

    assert (project_root / "sample-documents" / "HCLTECH_Q1_FY27.pdf").exists()
