"""STUDENT EDIT FILE 2 OF 3 — hybrid retrieval."""

def reciprocal_rank_fusion(rankings:list[list[str]], *, k:int=60)->list[tuple[str,float]]:
    """Combine ranked source-id lists using RRF.

    Score contribution = 1 / (k + rank), with rank starting at 1.
    Return highest score first, then source_id for deterministic ties.
    """
    pass
