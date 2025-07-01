# base/route.py

from flask import Blueprint, render_template, request, session, redirect, url_for
from pathlib import Path
from base.model.user_model import UserModel
from base.service import menu_service
from admin.service import customer_service
from apps.route import app_route
from admin.route import admin_route
from functools import wraps

template_path = Path(__file__).resolve().parents[0] / 'templates'
base_route = Blueprint('base', __name__, template_folder=template_path)

# Middleware to check admin access once per session
def admin_access_check():
    # Chỉ kiểm tra nếu admin_verified chưa có trong session
    if 'admin_verified' not in session:
        user = session.get('user')
        if not user or not user.get("is_admin", False):
            return redirect(url_for('base.index'))
        else:
            # Đánh dấu rằng đã xác minh admin trong session
            session['admin_verified'] = True
    return None

# Register blueprints
base_route.register_blueprint(app_route, url_prefix='/apps')

# Kiểm tra admin trước mỗi request tới admin routes
@admin_route.before_request
def verify_admin():
    return admin_access_check()

base_route.register_blueprint(admin_route, url_prefix='/admin')

def render_layout(type:int = 0):
    '''
    Render the layout based on the type of user.
    '''
    user_info = session.get('user')
    if user_info:
        user = UserModel(**user_info)
        menu = menu_service.get_menu(type)
        customer = customer_service.get_customer()
        # db_info_by_customer
        side = "/apps"
        if type == 1:
            side = "/admin"
            route = request.args.get('route', f"{side}/dashboard")
            template_name = 'admin.html'
        else:
            route = request.args.get('route', f"{side}/dashboard")
            template_name = 'index.html'            
        print(f"Route: {route}")
        return render_template(template_name, user=user, route=route, menu=menu, side=side, customers=customer)
    else:
        return redirect(url_for('auth.login'))
   
@base_route.route('/')
def index():
    return render_layout(0)

@base_route.route('/admin')
def admin():
    user = session.get('user')
    if not user:
        return redirect(url_for('auth.login'))
    elif user.get("is_admin") == False:  
        return redirect(url_for('base.index'))
    return render_layout(1)

@base_route.route('/error')
def error():
    return render_template('error.html')