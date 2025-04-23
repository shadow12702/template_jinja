import os
from flask import Blueprint, render_template, request, session, redirect, url_for
from admin.models.model_response import *
from admin.routes.route.config_route import config_route
from admin.routes.route.patch_route import patch_route
from apps.models.responses.user_model import UserModel
from admin.presentation.service import ApiService
from src.admin.routes.route.best_practice_route import best_practice_route
from src.admin.routes.route.awr_route import awr_route
from src.admin.routes.route.customer_route import customer_route


current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'templates')


# Khởi tạo blueprint với template_folder xác định
admin_route = Blueprint('admin_route', __name__, template_folder=template_dir)

admin_route.register_blueprint(customer_route)
admin_route.register_blueprint(awr_route)
admin_route.register_blueprint(best_practice_route)
admin_route.register_blueprint(patch_route)
admin_route.register_blueprint(config_route)

# Phần còn lại của code không thay đổi

@admin_route.route("/error")
def error():
    return render_template("error.html")

@admin_route.route("/admin")
def admin():
    user_data = session.get('user')
    user = UserModel(**user_data) if user_data else None
    menu = ApiService.get_menu(1)
    
    # Lấy route từ query parameter, mặc định là trang chính
    selected_route = request.args.get('route', '/error')
    
    return render_template("admin.html", user=user, menu=menu, selected_route=selected_route)

