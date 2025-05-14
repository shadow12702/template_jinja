from math import ceil
from flask import Blueprint, render_template, request, redirect, session, url_for
from admin.service import best_practice_service
from admin.model.request.best_practice_request import BestPracticeRequest 
from pathlib import Path

template_path = Path(__file__).resolve().parents[1] / 'templates/best_practice'
best_practice_route = Blueprint('best_practice', __name__, template_folder=template_path)

#---------------------------------------Get Best all Practice----------------------------#

@best_practice_route.route("/list")
def best_practice_management():
    _list = best_practice_service.get_best_practices()    
    return render_template("best_practices.html", best_practices=_list)

#---------------------------------------Add Best Practice----------------------------#

@best_practice_route.route("/add")
def add_best_practice():
    return render_template("add_best_practice.html")

#---------------------------------------Add Best Practice Action ----------------------------#

@best_practice_route.route("/add_new_best_practice", methods=["GET", "POST"])
def add_new_best_practice():
    _new_best_practice = BestPracticeRequest(**request.form)
    response = best_practice_service.add_best_practice_action(_new_best_practice)
    if response.status_code == 200:
        return url_for("best_practice_route.best_practice_management")  
    else:
        return render_template("add_best_practice.html" , error=f"Lỗi khi thêm best practice: {response.text}")

#--------------------------------------Detail Best Practice----------------------------#

@best_practice_route.route("/detail/<id>")
def detail_best_practice(id):
    best_practice = best_practice_service.get_best_practice_by_id(id)
    return render_template("detail_best.html", best_practice=best_practice)

#---------------------------------------Edit Best Practice----------------------------#

@best_practice_route.route("/update_info_best_practice/<id>", methods=["GET", "POST"])
def update_best_practice(id):
    _update_best_practice = BestPracticeRequest(**request.form)
    response = best_practice_service.update_best_practice_action(id, _update_best_practice)
    if response.status_code == 200:
        return redirect(url_for("base.admin.best_practice.best_practice_management", route="/best-practice"))
    else:
        best_practice = best_practice_service.get_best_practice_by_id(id)
        return render_template("detail_best.html", best_practice=best_practice,error=f"Lỗi khi cập nhật best practice: {response.text}")