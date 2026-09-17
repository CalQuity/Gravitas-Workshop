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
