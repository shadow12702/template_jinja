from pydantic import BaseModel

class UpdateCustomerRequest(BaseModel):
    Name: str 