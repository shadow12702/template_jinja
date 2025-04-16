import requests
from flask import request
# from core.auth_utils import validate_token
from core.app_setting import app_config

class RequestHandler:

    @staticmethod
    def post(endpoint, data=None, headers:dict={}):
        try:
            token = request.cookies.get('token')
            if token: 
                headers.update({'Authorization': f"Bearer {token}"})
            url = f'{app_config.apiUrl}/{app_config.version}{endpoint}'
            response = requests.post(url, json=data, headers=headers)
            return response
        except Exception as ex:
            raise ex
        
    @staticmethod
    def get(endpoint, headers:dict={}):
        try:
            token = request.cookies.get("token")
            if token:
                headers.update({'Authorization': f"Bearer {token}"})
            url = f'{app_config.apiUrl}/{app_config.version}{endpoint}'
            response = requests.get(url, headers)
            return response
        except Exception as ex:
            raise ex
    @staticmethod
    def put(endpoint, data=None, headers: dict = {}):
        try:
            token = request.cookies.get("token")
            if token:
                headers.update({'Authorization': f"Bearer {token}"})
            url = f"{app_config.apiUrl}/{app_config.version}{endpoint}"
            response = requests.put(url, json=data, headers=headers)
            return response
        except Exception as ex:
            raise ex
    @staticmethod
    def delete(endpoint, headers: dict = {}):
        try:
            token = request.cookies.get("token")
            if token:
                headers.update({'Authorization': f"Bearer {token}"})
            url = f"{app_config.apiUrl}/{app_config.version}{endpoint}"
            response = requests.delete(url, headers=headers)
            return response
        except Exception as ex:
            raise ex