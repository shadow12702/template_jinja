# 

from pydantic import BaseModel

class CustomerResponse(BaseModel):
    Code: str
    Name: str

