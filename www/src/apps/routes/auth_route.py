from flask import Blueprint, request, redirect, url_for, render_template, make_response, session
from core.auth_utils import refresh_token
from core.request import RequestHandler
from src.apps.models.responses.login_response import LoginResponse


auth_route = Blueprint('auth_route', __name__)

@auth_route.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        client_ip = request.remote_addr         #Client IP address

        response = RequestHandler.post(
            '/auth/login',
            data={"username": username, "password": password, "ip_address": client_ip }
            )
        if response.status_code == 200:
            login_resp = LoginResponse(**response.json())            
            session['user'] = login_resp.user.dict()
            resp = make_response(redirect(url_for("index_route.index")))
            resp.set_cookie('token', login_resp.token.access)
            resp.set_cookie('refresh', login_resp.token.refresh)
            return resp
        
    return render_template('login.html')

@auth_route.route('/logout', methods=['GET','POST'])
def logout():
    current_token = request.cookies.get('token')
    if not current_token:
        return redirect(url_for('auth_route.login'))
    response = RequestHandler.post(
        '/auth/logout',
        data={"token": current_token}
    )
    if response.status_code == 200:
        resp = make_response(redirect(url_for('auth_route.login')))
        resp.set_cookie('token', '', expires = 0)
        resp.set_cookie('refresh', '', expires=0)
        return resp
    return redirect(url_for('auth_route.login'))


@auth_route.route('/refresh', methods=['POST'])
def refresh():
    refresh = request.cookies.get('refresh')
    if not refresh:
        return redirect(url_for('auth_route.login'))
    current_page = request.referrer
    new_token = refresh_token(refresh)
    if new_token:
        resp = make_response(redirect(current_page))
        resp.set_cookie('token', new_token.token)
        return resp
    else:
        return redirect(url_for('auth_route.login'))