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


if __name__ == '__main__':
    sample_pages = [{'page': 1, 'text': 'Revenue grew 4.2% year over year. ' * 40}]
    chunks = chunk_pages(sample_pages, chunk_size=200, overlap=20)
    print(f'Chunked 1 sample page into {len(chunks)} chunks')
    if chunks:
        print('First chunk:', chunks[0]['text'][:150])
