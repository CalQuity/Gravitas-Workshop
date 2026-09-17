from pathlib import Path
import json
from langfuse import observe
from retrieval.ingestion.parsing import parse_pdf_pages
from retrieval.ingestion.chunking import chunk_pages
ROOT=Path(__file__).resolve().parents[2]
MANIFEST=ROOT/'data/corpus_manifest.json'
DOCS=ROOT/'data/documents'
PROCESSED=ROOT/'data/processed/chunks.jsonl'

def load_manifest(): return json.loads(MANIFEST.read_text())

def build_corpus(*, chunk_size=1200, overlap=120):
    records=[]
    for item in load_manifest():
        path=DOCS/item['filename']
        if not path.exists(): raise FileNotFoundError(f"Missing {path.name}. Run scripts/fetch_documents.py first.")
        pages=parse_pdf_pages(path)
        chunks=chunk_pages(pages,chunk_size=chunk_size,overlap=overlap)
        for c in chunks:
            sid=f"{item['id']}-p{c['page']}-c{c['chunk']}"
            records.append({**item,'source_id':sid,'page':c['page'],'chunk':c['chunk'],'text':c['text']})
    PROCESSED.parent.mkdir(parents=True,exist_ok=True)
    with PROCESSED.open('w',encoding='utf-8') as f:
        for r in records: f.write(json.dumps(r,ensure_ascii=False)+'\n')
    return records

def load_corpus():
    if not PROCESSED.exists(): raise FileNotFoundError('Processed corpus missing. Build it from the notebook first.')
    return [json.loads(x) for x in PROCESSED.read_text(encoding='utf-8').splitlines() if x.strip()]

@observe(name="read-source")
def read_source(source_id:str):
    for r in load_corpus():
        if r['source_id']==source_id: return r
    return None


if __name__ == '__main__':
    try:
        rows = load_corpus()
        print(f'Processed corpus present: {len(rows)} chunks')
        print('Example:', {k: rows[0][k] for k in ['source_id','company','period','doc_type','page']})
    except FileNotFoundError:
        print('No processed corpus yet. Run scripts/fetch_documents.py, then build_corpus() '
              '(see 03_indexing_and_rag.ipynb, Mission 6).')
