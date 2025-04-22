from pydantic import BaseModel

class CustomerRequest(BaseModel):
    code:str
    name: str 