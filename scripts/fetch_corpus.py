from pathlib import Path
import json, urllib.request
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'data/corpus_manifest.json').read_text())
out=ROOT/'data/documents'; out.mkdir(parents=True,exist_ok=True)
for item in manifest:
    dest=out/item['filename']
    if dest.exists() and dest.stat().st_size>1000:
        print('cached',dest.name); continue
    print('downloading',item['company'],item['doc_type'],item['period'])
    req=urllib.request.Request(item['url'],headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=90) as r:
        data=r.read()
    if not data.startswith(b'%PDF'):
        raise RuntimeError(f"Expected PDF for {item['url']}")
    dest.write_bytes(data)
    print('saved',dest.name, len(data),'bytes')
print('Corpus ready:', len(manifest),'official PDFs')
