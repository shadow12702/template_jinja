from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ConfigResponse(BaseModel):
    type: str
    key: str
    value: str
    is_locked: int
