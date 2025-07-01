from pydantic import BaseModel

class BestPracticeRequest(BaseModel):
    db_version: str
    parameter: str
    param_default_value: str
    param_recommend_value: str
    for_rac_only: bool
    notes: str = None