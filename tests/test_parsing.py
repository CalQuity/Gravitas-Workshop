from __future__ import annotations

import asyncio
from pathlib import Path
from types import SimpleNamespace

import pytest

import parsing


def test_parse_pdf_returns_plain_page_dictionaries(monkeypatch, tmp_path: Path) -> None:
    pdf = tmp_path / "results.pdf"
    pdf.write_bytes(b"%PDF-fake")
    parser_was_closed = False

    class FakeParser:
        def __init__(self, **kwargs):
            assert kwargs == {"output_format": "markdown", "quiet": True}

        def parse(self, path: Path):
            assert path == pdf
            return SimpleNamespace(
                pages=[
                    SimpleNamespace(page_num=1, markdown="# Revenue\n₹100", text=""),
                    SimpleNamespace(page_num=2, markdown="", text="Fallback text"),
                    SimpleNamespace(page_num=3, markdown="", text=""),
                ]
            )

        def close(self):
            nonlocal parser_was_closed
            parser_was_closed = True

    monkeypatch.setattr(parsing, "LiteParse", FakeParser)

    pages = asyncio.run(parsing.parse_pdf(pdf))

    assert pages == [
        {"page": 1, "text": "# Revenue\n₹100", "source_file": "results.pdf"},
        {"page": 2, "text": "Fallback text", "source_file": "results.pdf"},
    ]
    assert parser_was_closed is True


def test_parse_pdf_rejects_a_document_without_text(monkeypatch, tmp_path: Path) -> None:
    pdf = tmp_path / "empty.pdf"
    pdf.write_bytes(b"%PDF-fake")

    class FakeParser:
        def __init__(self, **kwargs):
            pass

        def parse(self, path: Path):
            return SimpleNamespace(pages=[])

        def close(self):
            pass

    monkeypatch.setattr(parsing, "LiteParse", FakeParser)

    with pytest.raises(ValueError, match="No readable text"):
        asyncio.run(parsing.parse_pdf(pdf))

