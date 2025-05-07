from flask import Blueprint, render_template, request, redirect, url_for, session
from admin.service import config_service
from pathlib import Path

template_path = Path(__file__).resolve().parents[1] / 'templates/config'
config_route = Blueprint('config', __name__, template_folder=template_path)

# Routes
@config_route.route("/")
def config_management():
    _list = config_service.get_all_configs()
    return render_template("config.html", configs=_list)