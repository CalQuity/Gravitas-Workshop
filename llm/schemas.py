from pydantic import BaseModel, Field
class Citation(BaseModel):
    source_id:str
    page:int|None=None
class ResearchAnswer(BaseModel):
    answer:str
    citations:list[Citation]=Field(default_factory=list)
    confidence:str=Field(pattern='^(low|medium|high)$')
