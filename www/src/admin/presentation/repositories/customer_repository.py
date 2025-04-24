from core.request import RequestHandler
from src.admin.models.model_response import CustomerResponse
from admin.models.model_request import CustomerRequest, UpdateCustomerRequest

class CustomerRepository():
    
    
    # Lấy danh sách tất cả khách hàng
    def get_customer():
        response = RequestHandler.post("/customer/get-customer", headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            customers = [CustomerResponse(**item) for item in response.json()]
            return customers
        return []


    # Lấy thông tin khách hàng theo mã code
    def get_customer_by_code(code):
        response = RequestHandler.get(f"/customer/show/{code}", headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            customers = [CustomerResponse(**item) for item in response.json()]
            return customers
        return []


    # Thêm mới một khách hàng
    def add_customer_action(CustomerRequest: CustomerRequest):
        data = {
            "code": CustomerRequest.code,
            "name": CustomerRequest.name,
        }
        response = RequestHandler.post(f"/customer/add", data=data, headers={"Content-Type": "application/json"})
        return response


    # Cập nhật thông tin khách hàng theo mã code
    def update_customer_action(code, UpdateCustomerRequest: UpdateCustomerRequest):
        data = {
            "name": UpdateCustomerRequest.name,
        }
        response = RequestHandler.put(f"/customer/update/{code}", data=data, headers={"Content-Type": "application/json"})
        return response
