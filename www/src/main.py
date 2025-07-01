# main.py

from flask import Flask, request
from base.auth_route import auth_route
from base.route import base_route
from core.auth_utils import validate_refresh_token
from core.app_setting import app_config
from core.socket_hub import SocketHub

app = Flask(__name__, static_folder='static', template_folder='base/templates') 
socketio = SocketHub(app, port=678)  # Khởi tạo SocketHub với Flask app

app.secret_key = app_config.secret_key

app.register_blueprint(base_route)
app.register_blueprint(auth_route)

@app.before_request
def before_request():
    print('before-request: ', request.endpoint)
    if request.endpoint in ('auth.login', 'auth.register', 'static'):
        return None
    response = validate_refresh_token()
    if response:
        return response


if __name__ == '__main__':
    socketio.run(app, debug=True)  # Chạy ứng dụng với SocketIO
    # app.run(debug=True)