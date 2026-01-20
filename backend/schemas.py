from pydantic import BaseModel

class ConvertRequest(BaseModel):
    query: str
