from student_work.indexing import make_pinecone_record

def test_make_pinecone_record_preserves_provenance():
    row={'source_id':'INFY-FY25-p3-c1','text':'Revenue grew 4.2%.','company':'Infosys','period':'FY25','doc_type':'results','filename':'infosys.pdf','page':3,'chunk':1}
    out=make_pinecone_record(row)
    assert out['_id']==row['source_id']
    for key in ['source_id','text','company','period','doc_type','filename','page']:
        assert out[key]==row[key]
