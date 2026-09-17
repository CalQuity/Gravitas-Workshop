from __future__ import annotations

import os
import re

from langfuse import observe
from pinecone import Pinecone
from rank_bm25 import BM25Okapi

from config import load_workshop_env
from retrieval.corpus import load_corpus


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
