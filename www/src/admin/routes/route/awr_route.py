from flask import Blueprint, redirect, render_template, session, url_for
import os

from src.admin.presentation.service import ApiService
from src.apps.models.responses.user_model import UserModel

# Tính toán đường dẫn chính xác đến thư mục chứa test.html
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'templates', 'awr_database')

awr_route = Blueprint('awr_route', __name__, template_folder=template_dir)

@awr_route.route("/awr")
def awr():
    user_data = session.get('user')
    menu = []
    customers = []
    db_repo_info = []
    
    if user_data:
        try:
            user = UserModel(**user_data)
            # Lấy dữ liệu menu
            menu = ApiService.get_menu(1)
            # Lấy dữ liệu khách hàng
            customers = ApiService.get_customer(0)
            # Lấy thông tin repo db
            db_repo_info = ApiService.get_db_repo_info(customers[0].code) if customers else []
            
            return render_template("awr_database.html", 
                                    user=user, 
                                    menu=menu, 
                                    customers=customers, 
                                    db_repo_info=db_repo_info)
        
        except Exception as ex:
            print(f"Lỗi trong route awr: {ex}")
            raise ex
    else:
        return redirect(url_for('auth_route.login'))