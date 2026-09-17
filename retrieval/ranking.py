import re

from langfuse import observe


@observe(name="rerank-candidates")
def rerank_candidates(query: str, hits: list[dict], *, top_k: int = 5) -> list[dict]:
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
