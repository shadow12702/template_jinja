from pydantic import BaseModel

class CustomerResponse(BaseModel):
    code: str
    name: str

