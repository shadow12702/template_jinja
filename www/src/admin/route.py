# admin/route.py

from flask import Blueprint, render_template , redirect, session, url_for
from pathlib import Path
from admin.routes.customer_route import customer_route
from admin.routes.awr_repo_route import awr_repo_route
from admin.routes.best_practice_route import best_practice_route
from admin.routes.patch_route import patch_route
from admin.routes.config_route import config_route

template_path = Path(__file__).resolve().parents[0] / 'templates'
admin_route = Blueprint('admin', __name__, template_folder=template_path)

admin_route.register_blueprint(customer_route, url_prefix='/customer')
admin_route.register_blueprint(awr_repo_route, url_prefix='/awr-db')
admin_route.register_blueprint(best_practice_route, url_prefix='/best-practice')
admin_route.register_blueprint(patch_route, url_prefix='/db-patch')
admin_route.register_blueprint(config_route, url_prefix='/config')


@admin_route.route('/dashboard')
def dashboard():
    return render_template('admin-dashboard.html')
