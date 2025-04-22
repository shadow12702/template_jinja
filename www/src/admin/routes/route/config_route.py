from flask import Blueprint, render_template, request, redirect, url_for, session
from core.request import RequestHandler
from src.admin.models.model_response import ConfigResponse
from apps.models.responses.user_model import UserModel
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'templates', 'config')

config_route = Blueprint('config_route', __name__, template_folder=template_dir)

def get_user_data():
    user_data = session.get('user')
    return UserModel(**user_data) if user_data else None

def get_all_configs():
    response = RequestHandler.post("/config/get-config", headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        return [ConfigResponse(**item) for item in response.json()]
    return []

def get_config_by_type_key(type_, key):
    response = RequestHandler.get(f"/config/show/{type_}/{key}", headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        return ConfigResponse(**response.json())
    return None

def add_config_action(data):
    return RequestHandler.post("/config/add", data=data, headers={"Content-Type": "application/json"})

def update_config_action(type_, key, data):
    return RequestHandler.put(f"/config/update/{type_}/{key}", data=data, headers={"Content-Type": "application/json"})


# Routes
@config_route.route("/config")
def config_management():
    configs = get_all_configs()
    return render_template("config_management.html", configs=configs, user=get_user_data())

@config_route.route("/add_config")
def add_config():
    return render_template("add_new_config.html", user=get_user_data())

@config_route.route("/add_new_config", methods=["POST"])
def add_new_config():
    data = {
        "type": request.form.get("type"),
        "key": request.form.get("key"),
        "value": request.form.get("value"),
        "is_locked": int(request.form.get("is_locked", 0))
    }
    response = add_config_action(data)
    if response.status_code == 200:
        return redirect(url_for("config_route.config_management"))
    return render_template("add_new_config.html", user=get_user_data(), error="Lỗi khi thêm config")

@config_route.route("/edit_config/<type_>/<key>", methods=["GET", "POST"])
def edit_config(type_, key):
    if request.method == "POST":
        data = {
            "value": request.form.get("value"),
            "is_locked": int(request.form.get("is_locked", 0))
        }
        response = update_config_action(type_, key, data)
        if response.status_code == 200:
            return redirect(url_for("config_route.config_management"))
        else:
            config = get_config_by_type_key(type_, key)
            return render_template("edit_config.html", config=config, user=get_user_data(), error="Lỗi khi cập nhật config")
    else:
        config = get_config_by_type_key(type_, key)
        return render_template("edit_config.html", config=config, user=get_user_data())
