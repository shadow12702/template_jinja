import requests
from flask import Blueprint, render_template, session,request
from model.login_response import MenuModel, UserModel

index_route = Blueprint('index_route', __name__)

def get_menu():
    try:
        token = request.cookies.get('token')
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "code": "",
            "name": "",
            "icon": "", 
            "parent": "",
            "route": "",
            "is_show": True
        }
        
        response = requests.post("http://138.2.82.108:8080/v1.0/menu/get-menu", 
                                 headers=headers, json=data)
        
        print(f"Response status: {response.status_code}, Response text: {response.text}")
        response.raise_for_status()
        
        return [MenuModel(**item) for item in response.json()]
    except requests.RequestException as e:
        print(f"API error: {e}")
        return []

@index_route.route("/")
def index():
    user_data = session.get('user')
    user = UserModel(**user_data) if user_data else None
    menu = get_menu()
    return render_template("index.html", user=user, menu=menu, datamoi=[])