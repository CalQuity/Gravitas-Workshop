from pathlib import Path
import json, sys, urllib.error, urllib.request

USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
)

ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'data/corpus_manifest.json').read_text())
out=ROOT/'data/documents'; out.mkdir(parents=True,exist_ok=True)
failed=[]
for item in manifest:
    dest=out/item['filename']
    if dest.exists() and dest.stat().st_size>1000:
        print('cached',dest.name); continue
    print('downloading',item['company'],item['doc_type'],item['period'])
    req=urllib.request.Request(item['url'],headers={'User-Agent':USER_AGENT})
    try:
        with urllib.request.urlopen(req,timeout=90) as r:
            data=r.read()
        if not data.startswith(b'%PDF'):
            raise RuntimeError(f"Expected PDF for {item['url']}")
    except (urllib.error.URLError, RuntimeError) as exc:
        print(f"  FAILED ({exc}) — skipping for now, will retry other documents")
        failed.append(item)
        continue
    dest.write_bytes(data)
    print('saved',dest.name, len(data),'bytes')

if failed:
    print(f"\n{len(failed)} of {len(manifest)} documents failed to download:")
    for item in failed:
        print(f"  - {item['company']} {item['doc_type']} {item['period']}: {item['url']}")
    print("Retry this script (e.g. from a different network) or ask a facilitator for a checkpoint.")
    sys.exit(1)
print('Corpus ready:', len(manifest),'official PDFs')
