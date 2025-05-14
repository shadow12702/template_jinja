# admin/service/customer_service.py

from core.request import RequestHandler
from admin.model.response.customer_response import CustomerResponse
from admin.model.request.customer_request import CustomerRequest


def get_customer_by_type(type: int):
    """
    Get customer information.
    """
    response = RequestHandler.post('/customer/get-customer', data={"type": type}, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        customer_data = response.json()
        customer = [CustomerResponse(**item) for item in customer_data]
        return customer
    return None

def get_customer():
    """
    Get customer information.
    """
    response = RequestHandler.post('/customer/get-customer', headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        customer_data = response.json()
        customer = [CustomerResponse(**item) for item in customer_data]
        return customer
    return None

def get_customer_by_code(code: str):
    """
    Get customer information by code.
    """
    try:
        if not code:
            raise ValueError("Code cannot be empty")
        response = RequestHandler.get(f'/customer/show/{code}', headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            return CustomerResponse(**response.json())
        return None
    except Exception as e:
        raise e
    
def add_customer(customer: CustomerRequest):
    """
    Add a new customer.
    """
    try:
        if not customer:
            raise ValueError("Customer cannot be empty")
        response = RequestHandler.post('/customer/add', data=customer.model_dump(), headers={"Content-Type": "application/json"})
        return response
    except Exception as e:
        raise e
    
def update_customer(code , customer: CustomerRequest):
    """
    Update customer information.
    """
    try:
        if not customer:
            raise ValueError("Customer cannot be empty")

        response = RequestHandler.put(f'/customer/update/{code}', data=customer.model_dump(), headers={"Content-Type": "application/json"})
        return response
    except Exception as e:
        raise e
    