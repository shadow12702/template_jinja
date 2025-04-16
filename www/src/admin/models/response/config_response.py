from pydantic import BaseModel
from datetime import datetime

class ConfigResponse(BaseModel):
    Type : str
    Key : str
    Value: str
    IsLocked: int
    CreatedOn : datetime
    LastChanged : datetime