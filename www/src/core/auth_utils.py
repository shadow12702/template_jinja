from flask import  make_response, redirect, request, url_for
from core.request import RequestHandler
from model.login_response import RefreshTokenResponse

def validate_refresh_token():
    '''Validate and refresh token when token expired'''
    token = request.cookies.get('token')
    refresh = request.cookies.get('refresh')

    if not token:
        return redirect(url_for('auth_route.login'))
    if validate_token(token):
        return None
    
    new_token = refresh_token(refresh)
    if new_token:
        response = make_response()
        response.set_cookie('token', new_token.token)
        return response
    else:
        return redirect(url_for('auth_route.login'))

    
def validate_token(token: str):
    response = RequestHandler.post('/auth/verify_token', data={"token": token})
    return response.status_code == 200

def refresh_token(refresh:str):
    response = RequestHandler.post('/auth/refresh-token',data={"token": refresh})
    if response.status_code == 200:
        return RefreshTokenResponse(**response.json())
    return None