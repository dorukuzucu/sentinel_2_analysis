from pydantic import BaseModel


class AnalysisRequest(BaseModel):
    name: str
