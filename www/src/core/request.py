import requests
from flask import request
# from core.auth_utils import validate_token
from core.app_setting import app_config

class RequestHandler:

    @staticmethod
    def post(endpoint, data=None, headers=None):
        token = request.cookies.get('token')
        if token: 
            headers = {'Authenticator': f"Bearer {token}"}
        url = f'{app_config.apiUrl}/{app_config.version}{endpoint}'
        response = requests.post(url, json=data, headers=headers)
        return response
    
    @staticmethod
    def get(endpoint, headers=None):
        token = request.cookies.get("token")
        if token:
            headers = {'Authenticator': f"Bearer {token}"}
        url = f'{app_config.apiUrl}/{app_config.version}{endpoint}'
        response = requests.get(url, headers)