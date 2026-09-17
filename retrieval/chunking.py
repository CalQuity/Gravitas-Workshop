from agno.knowledge.chunking.recursive import RecursiveChunking
from agno.knowledge.document import Document

def chunk_pages(pages: list[dict], *, chunk_size:int=1200, overlap:int=120) -> list[dict]:
    strategy=RecursiveChunking(chunk_size=chunk_size, overlap=overlap)
    out=[]
    for page in pages:
        doc=Document(name=f"page-{page['page']}",content=page['text'],meta_data={'page':page['page']})
        for i,ch in enumerate(strategy.chunk(doc),start=1):
            out.append({'page':page['page'],'chunk':i,'text':ch.content})
    return out
