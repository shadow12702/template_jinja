from pydantic import BaseModel

class CustomerRequest(BaseModel):
    Code:str
    Name: str 