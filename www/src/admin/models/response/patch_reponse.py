from typing import Optional
from pydantic import BaseModel

class PatchResponse(BaseModel):
    DbVersion: str
    Type: str
    Format: str
    PatchRoot: int
    PatchID: int
    PatchType: str
    FixedInRu: Optional[str] = None
    FixedInMRP: Optional[str] = None
    Description: Optional[str] = None
