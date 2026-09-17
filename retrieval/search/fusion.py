"""Reciprocal Rank Fusion: combine ranked lists from different retrievers.

This is also the reference implementation for Mission 9's notebook exercise —
try writing your own version in the notebook first, then compare it against
this one before it's used for real in the hybrid-retrieval pipeline below.
"""


def reciprocal_rank_fusion(rankings: list[list[str]], *, k: int = 60) -> list[tuple[str, float]]:
    """Combine ranked source-id lists using RRF.

    Score contribution = 1 / (k + rank), with rank starting at 1.
    Returns highest score first, then source_id for deterministic ties.
    """
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, source_id in enumerate(ranking, start=1):
            scores[source_id] = scores.get(source_id, 0.0) + 1 / (k + rank)
    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))


if __name__ == '__main__':
    print(reciprocal_rank_fusion([['a', 'b', 'c'], ['b', 'd', 'a']]))
