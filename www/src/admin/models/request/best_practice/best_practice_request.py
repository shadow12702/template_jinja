from pydantic import BaseModel

class BestPracticeRequest(BaseModel):
    BPDbVersion: str
    BPParameter: str
    BPParamDefaultValue: str
    BPParamRecommendValue: str
    BPForRacOnly: int
    BPNotes: str = None