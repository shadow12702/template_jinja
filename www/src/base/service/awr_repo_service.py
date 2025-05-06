# admin/service/awr_repo_service.py

from admin.model.response.awr_repo_customer_response import AwrRepoCustomerResponse
from core.request import RequestHandler

def get_awr_repo():
    """
    Get AWR repository information.
    """
    response = RequestHandler.post('/awr/get-awr-repo-info', headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        return response.json()
    return None

def get_awr_repo_by_customer(customer_code: str):
    """
    Get AWR repository information by customer code.
    """
    try:
        if not customer_code:
            raise ValueError("Customer code cannot be empty")
        response = RequestHandler.post('/awr/get-awr-repo-by-customer', data={"customer_code": customer_code}, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            data = [
                AwrRepoCustomerResponse(**item) for item in response.json()
            ]
            return data
        return None
    except Exception as e:
        raise e
    
