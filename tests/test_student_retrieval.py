from student_work.retrieval import reciprocal_rank_fusion

def test_rrf_combines_rankings():
    out=reciprocal_rank_fusion([['a','b','c'],['b','d','a']],k=60)
    assert out[0][0] in {'a','b'}
    scores=dict(out)
    assert scores['a']>scores['c'] and scores['b']>scores['d']
