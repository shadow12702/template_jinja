from flask import Flask, request
import os
from jinja2 import ChoiceLoader, FileSystemLoader
from core.auth_utils import validate_refresh_token
from core.app_setting import app_config
from apps.routes.auth_route import auth_route
from apps.routes.index_route import index_route
from apps.routes.dashboard_route import db_route
from apps.routes.chart_route import chart_route
from admin.routes.admin_route import admin_route

# Xác định đường dẫn gốc của project
basedir = os.path.abspath(os.path.dirname(__file__))

# Cấu hình đường dẫn tới thư mục templates
template_folder_users = os.path.join(basedir, 'apps', 'templates')
template_folder_admin = os.path.join(basedir, 'admin', 'templates')
static_folder = os.path.join(basedir, 'static')

# Khởi tạo Flask app
app = Flask(__name__, 
           template_folder=template_folder_users,  # Sử dụng một thư mục mặc định
           static_folder=static_folder)

# Cấu hình nhiều thư mục templates
app.jinja_loader = ChoiceLoader([
    FileSystemLoader(template_folder_users),
    FileSystemLoader(template_folder_admin),
    FileSystemLoader(os.path.join(basedir, 'templates')) 
])

chart_blueprint = {}
charts = {}

app.secret_key = app_config.secret_key

app.register_blueprint(auth_route)
app.register_blueprint(index_route)
app.register_blueprint(db_route)
app.register_blueprint(chart_route)
app.register_blueprint(admin_route)

# Register before_request hook
@app.before_request
def before_request():
    if request.endpoint == 'auth_route.login':
        return None
    response = validate_refresh_token()
    if response:
        return response

if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)    