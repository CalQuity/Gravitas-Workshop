def build_context(hits:list[dict], *, max_chars:int=9000)->str:
    blocks=[]; used=0
    for h in hits:
        b=f"[{h['source_id']}] {h.get('company')} | {h.get('doc_type')} | {h.get('period')} | page {h.get('page')}\n{h.get('text','')}"
        if used+len(b)>max_chars: break
        blocks.append(b); used+=len(b)
    return '\n\n'.join(blocks)
