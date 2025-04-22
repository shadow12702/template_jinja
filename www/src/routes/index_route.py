import requests
from flask import Blueprint, render_template, session,request
from model.login_response import MenuModel, UserModel
from flask import Blueprint, render_template, session, request, redirect, url_for
from model.login_response import AwrRepoInfoResponse, CustomerResponse, MenuModel, UserModel
from core.request import RequestHandler

index_route = Blueprint('index_route', __name__)

@index_route.route("/")
def index():
    user_data = session.get('user')
    menu = []
    customers = []
    AwrRepoInfo = []
    if user_data:
        try:
            user = UserModel(**user_data)
            
            # Lấy dữ liệu menu
            menu_response = RequestHandler.post("/menu/get-menu", 
                                            data={"type": 0}, 
                                            headers={"Content-Type": "application/json"})
            
            if menu_response.status_code == 200:
                menu = [MenuModel(**item) for item in menu_response.json()]
            
            # Lấy dữ liệu khách hàng
            customer_response = RequestHandler.post("/customer/get-customer", 
                                                headers={"Content-Type": "application/json"})
            
            if customer_response.status_code == 200:
                customer_data = customer_response.json()
                print(f"Dữ liệu khách hàng: {customer_data}")  # In dữ liệu để kiểm tra
                customers = [CustomerResponse(**item) for item in customer_data]


            cusdb_response = RequestHandler.post("/awr/get-awr-repo-info", 
                                                headers={"Content-Type": "application/json"})
            
            if cusdb_response.status_code == 200:
                cusDb_data = cusdb_response.json()
                print(f"Dữ liệu Db: {cusDb_data}")  # In dữ liệu để kiểm tra
                AwrRepoInfo = [AwrRepoInfoResponse(**item) for item in cusDb_data]
            
            return render_template("index.html", user=user, menu=menu, customers=customers, AwrRepoInfo=AwrRepoInfo)
        
        except Exception as ex:
            print(f"Lỗi trong route index: {ex}")
            raise ex
    else:
        return redirect(url_for('auth_route.login'))

@index_route.route("/profile")
def profile():
    user_data = session.get('user')
    user = UserModel(**user_data) if user_data else None
    if not user:
        return redirect(url_for('auth_route.login'))
    
    # You can fetch additional user profile data from API if needed
    # For now, we're just using the session data
    
    return render_template("profile.html", Username=user.Username if user else "")