import json
from llm.schemas import ResearchAnswer

def build_messages(question:str, context:str|None=None):
    system='You are a careful financial research assistant. Do not invent facts. If evidence is provided, use only that evidence and cite source IDs.'
    if context: system += '\n\nEVIDENCE:\n'+context
    return [{'role':'system','content':system},{'role':'user','content':question}]

def parse_structured_answer(text:str)->ResearchAnswer:
    return ResearchAnswer.model_validate(json.loads(text))
