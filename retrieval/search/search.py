from __future__ import annotations

import os
import re

from langfuse import observe
from pinecone import Pinecone, RerankModel
from rank_bm25 import BM25Okapi

from config import load_workshop_env
from retrieval.ingestion.corpus import load_corpus


def _tok(s):
    return re.findall(r"[a-z0-9.%$₹-]+", s.lower())


@observe(name="keyword-search")
def keyword_search(query: str, top_k: int = 8):
    rows = load_corpus()
    corpus = [_tok(r["text"]) for r in rows]
    bm25 = BM25Okapi(corpus)
    scores = bm25.get_scores(_tok(query))
    order = sorted(range(len(rows)), key=lambda i: scores[i], reverse=True)[:top_k]
    return [
        {**rows[i], "score": float(scores[i]), "retriever": "keyword"}
        for i in order
        if scores[i] > 0
    ]


@observe(name="pinecone-search")
def pinecone_search(query: str, top_k: int = 8, *, filter: dict | None = None):
    load_workshop_env()
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    idx = pc.index(os.getenv("PINECONE_INDEX", "gravitas-finresearch"))
    search_kwargs = {
        "namespace": os.getenv("PINECONE_NAMESPACE", "workshop"),
        "top_k": top_k,
        "inputs": {"text": query},
        "fields": ["source_id","text","company","period","doc_type","filename","page"],
    }
    if filter:
        search_kwargs["filter"] = filter
    resp = idx.search(**search_kwargs)
    out = []
    for hit in resp.result.hits:
        item = dict(hit.fields or {})
        item.setdefault(
            "source_id",
            getattr(hit, "id", None) or getattr(hit, "_id", None),
        )
        item["score"] = float(hit.score)
        item["retriever"] = "dense"
        out.append(item)
    return out


@observe(name="pinecone-rerank")
def pinecone_rerank(query: str, hits: list[dict], *, top_k: int = 5) -> list[dict]:
    """Rerank hits with Pinecone's own hosted reranking model (free-tier eligible).

    Unlike `retrieval/search/ranking.py`'s transparent lexical-overlap scorer
    (great for understanding *what* reranking does), this calls a real semantic
    reranker hosted by Pinecone — it reads each hit's text against the query and
    returns a relevance score, no local scoring logic involved.
    """
    load_workshop_env()
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    result = pc.inference.rerank(
        model=RerankModel.Pinecone_Rerank_V0,
        query=query,
        documents=hits,
        rank_fields=["text"],
        top_n=top_k,
    )
    reranked = []
    for match in result.data:
        item = dict(hits[match.index])
        item["rerank_score"] = match.score
        reranked.append(item)
    return reranked


if __name__ == '__main__':
    load_workshop_env()
    sample_query = 'What FY26 revenue growth guidance did Infosys give?'
    try:
        keyword_hits = keyword_search(sample_query, top_k=3)
        print(f'Keyword search: {len(keyword_hits)} hits')
        for h in keyword_hits:
            print('-', h['source_id'], h['text'][:100].replace('\n', ' '))
    except FileNotFoundError:
        print('Keyword search needs a processed corpus first — see retrieval/ingestion/corpus.py.')

    try:
        dense_hits = pinecone_search(sample_query, top_k=3)
        print(f'\nPinecone search: {len(dense_hits)} hits')
        for h in dense_hits:
            print('-', h['source_id'], h['text'][:100].replace('\n', ' '))
    except Exception as exc:
        print(f'\nPinecone search not available yet ({exc}). '
              'Run `uv run python -m retrieval.ingestion.index_corpus` first and confirm PINECONE_API_KEY is set.')

    try:
        toy_hits = [
            {'source_id': 'a', 'text': 'Revenue grew 4.2% in FY25.'},
            {'source_id': 'b', 'text': 'Margins were broadly stable.'},
            {'source_id': 'c', 'text': 'HCLTech guided FY26 revenue growth of 2-5% in constant currency.'},
        ]
        print(f'\nPinecone rerank of a toy shortlist for: {sample_query!r}')
        for h in pinecone_rerank(sample_query, toy_hits, top_k=3):
            print('-', h['source_id'], round(h['rerank_score'], 4), h['text'])
    except Exception as exc:
        print(f'\nPinecone rerank not available yet ({exc}).')
