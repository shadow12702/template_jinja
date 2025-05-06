from typing import Optional
from pydantic import BaseModel

class BestPracticeResponse(BaseModel):
    ''' A class to represent the response of a best practice. '''
    
    id: int
    db_version: str
    parameter: str
    param_default_value: str
    param_recommend_value: str
    for_rac_only: int
    notes: Optional[str] = None