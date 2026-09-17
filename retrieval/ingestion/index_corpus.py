"""Index the processed corpus into Pinecone.

`make_pinecone_record` is also the reference implementation for Mission 7's
notebook exercise — try writing your own version in the notebook first, then
compare it against this one.
"""

import os
import time

from pinecone import Pinecone
from pinecone.errors.exceptions import RateLimitError

from config import load_workshop_env
from retrieval.ingestion.corpus import load_corpus


def make_pinecone_record(row: dict) -> dict:
    """Preserve text + citation metadata when crossing into the vector index."""
    return {
        '_id': row['source_id'],
        'text': row['text'],
        'source_id': row['source_id'],
        'company': row['company'],
        'period': row['period'],
        'doc_type': row['doc_type'],
        'filename': row['filename'],
        'page': row['page'],
    }


def upsert_with_backoff(idx, *, namespace, records, max_retries=6):
    """Upsert one batch, retrying with backoff if Pinecone's embedding rate limit is hit.

    The free tier caps tokens/minute for the integrated embedding model, which a
    plain loop over batches can exceed. Pinecone reports how long to wait via
    `retry_after`; fall back to exponential backoff if that's not provided.
    """
    delay = 5
    for attempt in range(1, max_retries + 1):
        try:
            idx.upsert_records(namespace=namespace, records=records)
            return
        except RateLimitError as exc:
            if attempt == max_retries:
                raise
            wait = getattr(exc, 'retry_after', None) or delay
            print(f'  Rate limited by Pinecone, waiting {wait:.0f}s (attempt {attempt}/{max_retries})...')
            time.sleep(wait)
            delay = min(delay * 2, 60)


def main():
    load_workshop_env()
    rows = load_corpus()
    pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
    name = os.getenv('PINECONE_INDEX', 'gravitas-finresearch')
    namespace = os.getenv('PINECONE_NAMESPACE', 'workshop')

    # Pinecone v10+: integrated embedding indexes are created with create_for_model().
    # The call waits for the index to become ready by default.
    if not pc.indexes.exists(name):
        print(f'Creating Pinecone index {name} with integrated embeddings...')
        pc.indexes.create_for_model(
            name=name,
            cloud='aws',
            region='us-east-1',
            embed={
                'model': 'llama-text-embed-v2',
                'field_map': {'text': 'text'},
            },
            timeout=120,
        )

    idx = pc.index(name=name)
    batch = []
    indexed = 0
    for row in rows:
        batch.append(make_pinecone_record(row))
        if len(batch) >= 96:
            upsert_with_backoff(idx, namespace=namespace, records=batch)
            indexed += len(batch)
            print(f'  Indexed {indexed}/{len(rows)} chunks...')
            batch = []
            time.sleep(2)  # stay comfortably under the free tier's embedding tokens/minute limit
    if batch:
        upsert_with_backoff(idx, namespace=namespace, records=batch)
        indexed += len(batch)
    print(f'Indexed {len(rows)} chunks into {name}/{namespace}')


if __name__ == '__main__':
    main()
