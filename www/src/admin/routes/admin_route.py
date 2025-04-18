import os
from flask import Blueprint, render_template, request, session, redirect, url_for
from admin.models.model_response import *
from apps.models.responses.user_model import UserModel
from admin.presentation.service import ApiService
from core.request import RequestHandler
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

# Phần còn lại của code không thay đổi

@admin_route.route("/admin")
def admin():
    user_data = session.get('user')
    user = UserModel(**user_data) if user_data else None
    menu = ApiService.get_menu(1)

    return render_template("admin.html", user=user, menu=menu )


