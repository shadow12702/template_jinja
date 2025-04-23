from pydantic import BaseModel
from datetime import datetime

class ConfigRequest(BaseModel):
    value: str