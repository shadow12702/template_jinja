# services.py
from flask import session
from admin.models.response.awr_repo_info_response import AwrRepoInfoResponse
from admin.models.response.customer_response import CustomerResponse
from apps.models.responses.menu_model import MenuModel
from core.request import RequestHandler


class ApiService:
    @staticmethod
        
    def get_menu(type: int):
        # Gọi API để lấy menu
        response = RequestHandler.post("/menu/get-menu", data={"type": type}, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            menu = [MenuModel(**item) for item in response.json()]
            # Process the menu to flag if an item has children
            for item in menu:
                item.has_children = any(child.parent == item.code for child in menu)
                if item.has_children:
                    item.route = None  
            return menu
        return []   
    
    @staticmethod
    def get_customer(type:int):
        # Gọi API để lấy danh sách khách hàng
        response = RequestHandler.post("/customer/get-customer", headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            return [CustomerResponse(**item) for item in response.json()]
        return []
    @staticmethod
    def admin_required():
        ath = session['user']["IsAdmin"]
        if ath == True : return 1 
        else : return 0  
    @staticmethod
    def get_db_repo_info(customer_code: str):
        # Gọi API để lấy danh sách khách hàng
        response = RequestHandler.post("/awr/get-awr-repo-info", 
                                        data={"customer_code": customer_code},
                                        headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            return [AwrRepoInfoResponse(**item) for item in response.json()]
        return []