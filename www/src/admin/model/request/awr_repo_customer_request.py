# admin/model/request/awr_repo_customer_request.py

from pydantic import BaseModel

class AwrRepoCustomerRequest(BaseModel):
    """
    A class to represent a request for AWR repository by customer.
    """
    customer_code: str
    