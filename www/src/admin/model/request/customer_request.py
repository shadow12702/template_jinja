# admin/model/request/customer_request.py

from pydantic import BaseModel

class CustomerRequest(BaseModel):
    code: str
    name: str
    