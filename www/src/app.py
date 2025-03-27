from flask import Flask, request
from core.auth_utils import validate_refresh_token
from core.app_setting import app_config
from routes.index_route import index_route
from routes.auth_route import auth_route
from routes.dashboard_route import db_route

app = Flask(__name__)
chart_blueprint = {}
charts = {}

app.secret_key = app_config.secret_key

app.register_blueprint(auth_route)
app.register_blueprint(index_route)
app.register_blueprint(db_route)


# Register before_request hook
@app.before_request
def before_request():
    if request.endpoint == 'auth_route.login':
        return None
    response = validate_refresh_token()
    if response:
        return response

if __name__=="__main__":
    app.run(host="localhost", port=5001, debug=True)
