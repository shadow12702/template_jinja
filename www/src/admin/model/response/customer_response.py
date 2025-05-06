# admin/model/response/customer_response.py

from pydantic import BaseModel

class CustomerResponse(BaseModel):
    """
    A class to represent a customer response.
    """
    code: str
    name: str