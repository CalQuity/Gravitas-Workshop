"""A deliberately transparent reranker: spend a little more compute on a small,
already-fused shortlist rather than trusting the first-stage ranking as final.

Production systems often swap this for a learned cross-encoder reranker — the
scoring logic here is intentionally simple so the ranking stage stays inspectable.
"""

import re

from langfuse import observe


@observe(name="rerank-candidates")
def rerank_candidates(query: str, hits: list[dict], *, top_k: int = 5) -> list[dict]:
    """Score a shortlist of hits by how many query words they actually contain, then keep the best few.

    Walked through step by step:

    1. Split the query into lowercase "words" (`q`) — really just alphanumeric-ish
       tokens, so "24.3%" or "₹120" count as single tokens too. `re.findall` with
       that character class pulls all of them out at once.
    2. For each hit, do the same to its text (`terms`).
    3. `coverage = len(q & terms) / len(q)` — the `&` is a *set intersection*: it's
       the words that appear in **both** the query and the hit's text. Dividing by
       the size of the query's own word set turns that into a fraction from 0.0
       (no overlap at all) to 1.0 (every query word showed up in this hit).
       `(len(q) or 1)` just avoids a divide-by-zero if the query was empty.
    4. `rerank_score = coverage + 0.05 * score` — coverage does almost all of the
       work; the hit's incoming `score` (from dense or keyword search) is added in
       at a small (5%) weight, so it only acts as a *tiebreaker* between two hits
       with similar coverage — it can't outweigh a genuinely better lexical match.
    5. Sort by `rerank_score` descending (`-x["rerank_score"]`, since `sort`/`sorted`
       in Python always go smallest-first, so negating flips it to biggest-first),
       then by `source_id` as a tiebreaker so the order is deterministic when two
       hits score exactly the same. Keep only the top `top_k`.

    This is intentionally simple — a real production reranker is usually a
    trained model — but it makes the ranking stage fully inspectable: you can
    print `rerank_score` and see exactly why one hit outranked another.
    """
    q = set(re.findall(r"[a-z0-9.%$₹-]+", query.lower()))
    scored = []
    for hit in hits:
        terms = set(re.findall(r"[a-z0-9.%$₹-]+", hit.get("text", "").lower()))
        coverage = len(q & terms) / (len(q) or 1)
        item = dict(hit)
        item["rerank_score"] = coverage + 0.05 * float(hit.get("score", 0))
        scored.append(item)
    return sorted(
        scored,
        key=lambda x: (-x["rerank_score"], x.get("source_id", "")),
    )[:top_k]


if __name__ == '__main__':
    from config import load_workshop_env
    load_workshop_env()

    toy_hits = [
        {'source_id': 'a', 'text': 'Revenue grew 4.2% in FY25.', 'score': 0.7},
        {'source_id': 'b', 'text': 'Margins were broadly stable.', 'score': 0.9},
    ]
    for hit in rerank_candidates('revenue growth FY25', toy_hits):
        print(hit['source_id'], round(hit['rerank_score'], 3), hit['text'])
