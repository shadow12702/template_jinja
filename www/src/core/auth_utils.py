from datetime import datetime
from flask import  make_response, redirect, request, url_for
from core.request import RequestHandler
from apps.model.response.refresh_token_response import RefreshTokenResponse
from jose import jwt

def validate_refresh_token():
    '''Validate and refresh token when token expired'''
    token = request.cookies.get('token')
    refresh = request.cookies.get('refresh')

    if not token:
        return redirect(url_for('auth.login'))

    # check token expired
    if validate_token(token):
        if verify_token(token):
            return redirect(url_for('auth.login'))
        new_token = refresh_token(refresh)
        if new_token:
            response = make_response()
            response.set_cookie('token', new_token.token)
            return response
        else:
            return redirect(url_for('auth.login'))

    
def verify_token(token: str):
    response = RequestHandler.post('/auth/verify_token', data={"token": token})
    return response.status_code == 200

def refresh_token(refresh:str):
    response = RequestHandler.post('/auth/refresh-token',data={"token": refresh})
    if response.status_code == 200:
        return RefreshTokenResponse(**response.json())
    return None

def validate_token(token: str):
    try:
        payload =  jwt.get_unverified_claims(token)
        expired = payload.get("exp")
        return  datetime.now() > datetime.fromtimestamp(expired)
    except Exception as ex:
        print(f"Error verifying token: {ex}")
        return True
