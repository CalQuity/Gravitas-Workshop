from langfuse import observe

from retrieval.search import keyword_search, pinecone_search
from retrieval.ranking import rerank_candidates
from retrieval.corpus import read_source
from student_work.retrieval import reciprocal_rank_fusion


@observe(name="search-documents")
def search_documents(query: str, top_k: int = 5):
    dense = pinecone_search(query, top_k=max(8, top_k * 2))
    keyword = keyword_search(query, top_k=max(8, top_k * 2))
    by_id = {h["source_id"]: h for h in dense + keyword}
    fused = reciprocal_rank_fusion(
        [[h["source_id"] for h in dense], [h["source_id"] for h in keyword]]
    )
    candidates = []
    for sid, score in fused:
        if sid in by_id:
            item = dict(by_id[sid])
            item["score"] = score
            candidates.append(item)
    return rerank_candidates(query, candidates, top_k=top_k)
