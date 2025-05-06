# admin/route.py

from functools import wraps
from flask import Blueprint, render_template, request, redirect, session, url_for
from pathlib import Path
from admin.routes.customer_route import customer_route
from admin.routes.awr_repo_route import awr_repo_route


template_path = Path(__file__).resolve().parents[0] / 'templates'
admin_route = Blueprint('admin', __name__, template_folder=template_path)

admin_route.register_blueprint(customer_route, url_prefix='/customer')
admin_route.register_blueprint(awr_repo_route, url_prefix='/awr-repo')

def authorize():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = session.get('user')
            if not user or not user.get('is_admin'):
                return render_template('dashboard.html')
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@admin_route.route('/dashboard')
@authorize()
def dashboard():
    return render_template('admin-dashboard.html')

