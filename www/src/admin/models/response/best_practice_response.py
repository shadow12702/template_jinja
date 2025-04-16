from pydantic import BaseModel
from typing import Optional

class BestPracticeResponse(BaseModel):
    ID : int
    BPDbVersion: str
    BPParameter: str
    BPParamDefaultValue: str
    BPParamRecommendValue: str
    BPForRacOnly: int
    BPNotes: Optional[str] = None