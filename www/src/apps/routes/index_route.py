from flask import Blueprint, render_template, request, session, redirect, url_for
from core.request import RequestHandler
from src.admin.models.response.awr_repo_info_response import AwrRepoInfoResponse
from src.admin.models.response.customer_response import CustomerResponse
from src.apps.models.responses.menu_model import MenuModel
from src.apps.models.responses.user_model import UserModel
from admin.presentation.service import ApiService

index_route = Blueprint('index_route', __name__)


@index_route.route("/")
def index():
    user_data = session.get('user')
    menu = []
    customers = []
    db_repo_info = []
    if user_data:
        try:
            user = UserModel(**user_data)
            # Lấy dữ liệu menu
            menu = ApiService.get_menu(0) 
            # Lấy dữ liệu khách hàng
            customers = ApiService.get_customer(0)
            db_repo_info = ApiService.get_db_repo_info(customers[0].code) if customers else []
            
            selected_route = request.args.get('route', '/dashboard') 
            return render_template("index.html", selected_route = selected_route,
                                    user=user, menu=menu, customers=customers, db_repo_info=db_repo_info)
        
        except Exception as ex:
            print(f"Lỗi trong route index: {ex}")
            raise ex
    else:
        return redirect(url_for('auth_route.login'))




