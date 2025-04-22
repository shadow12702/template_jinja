from pydantic import BaseModel

class UpdateCustomerRequest(BaseModel):
    name: str 