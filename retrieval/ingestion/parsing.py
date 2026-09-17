from pathlib import Path
from liteparse import LiteParse

def parse_pdf_pages(path: str | Path, *, ocr_enabled: bool=False) -> list[dict]:
    parser=LiteParse(output_format='text',ocr_enabled=ocr_enabled,quiet=True)
    result=parser.parse(Path(path))
    pages=[]
    for p in result.pages:
        text=' '.join(x.text.strip() for x in p.text_items if getattr(x,'text','').strip())
        if text: pages.append({'page':int(p.page_num),'text':text})
    return pages


if __name__ == '__main__':
    ROOT = Path(__file__).resolve().parents[2]
    pdfs = sorted((ROOT / 'data/documents').glob('*.pdf'))
    if not pdfs:
        print('No PDFs in data/documents/ yet. Run scripts/fetch_documents.py first.')
    else:
        pages = parse_pdf_pages(pdfs[0])
        print(f'Parsed {pdfs[0].name}: {len(pages)} pages')
        if pages:
            print('First page snippet:', pages[0]['text'][:300])
