from flask import Blueprint, render_template, request, redirect, session, url_for
from admin.models.response.best_practice_response import BestPracticeResponse
from apps.models.responses.user_model import UserModel
from core.request import RequestHandler

from admin.models.model_request import BestPracticeRequest 
import os

# Định nghĩa đường dẫn cho template
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'templates', 'best_practice')

best_practice_route = Blueprint('best_practice_route', __name__, template_folder=template_dir)


def get_best_practices():
    response = RequestHandler.post("/best-practice/get-all", headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        best_practices = [BestPracticeResponse(**item) for item in response.json()]
        return best_practices
    return []


def get_best_practice_by_id(id):
    response = RequestHandler.get(f"/best-practice/show/{id}", headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        best_practice = [BestPracticeResponse(**item) for item in response.json()]
        return best_practice
    return []


def add_best_practice_action(best_practice_request: BestPracticeRequest):
    data = best_practice_request.dict()
    response = RequestHandler.post(f"/best-practice/add", data=data, headers={"Content-Type": "application/json"})
    return response


def update_best_practice_action(id, best_practice_request: BestPracticeRequest):
    data = best_practice_request.dict()
    response = RequestHandler.put(f"/best-practice/update/{id}", data=data, headers={"Content-Type": "application/json"})
    return response


def get_user_data():
    user_data = session.get('user')
    user = UserModel(**user_data)
    return user




#---------------------------------------Get Best all Practice----------------------------#

@best_practice_route.route("/best-practice")
def best_practice_management():
    best_practices = get_best_practices()
    return render_template("best_practice_management.html", best_practices=best_practices, user=get_user_data())

#---------------------------------------Add Best Practice----------------------------#

@best_practice_route.route("/add_best_practice")
def add_best_practice():
    return render_template("add_new_best_practice.html", user=get_user_data())

#---------------------------------------Add Best Practice Action ----------------------------#

@best_practice_route.route("/add_new_best_practice", methods=["GET", "POST"])
def add_new_best_practice():
    best_practice_request = BestPracticeRequest(
        db_version=request.form.get("db_version"),
        parameter=request.form.get("parameter"),
        param_default_value=request.form.get("param_default_value"),
        param_recommend_value=request.form.get("param_recommend_value"),
        for_rac_only=request.form.get("for_rac_only"),
        notes=request.form.get("notes")
    )
    response = add_best_practice_action(best_practice_request)
    
    if response.status_code == 200:
        return url_for("best_practice_route.best_practice_management")  
    else:
        return render_template("add_new_best_practice.html", user=get_user_data(), error=f"Lỗi khi thêm best practice: {response.text}")

#--------------------------------------Detail Best Practice----------------------------#

@best_practice_route.route("/detail_best_practice/<id>")
def detail_best_practice(id):
    best_practice = get_best_practice_by_id(id)
    return render_template("update_best_practice.html", best_practice=best_practice, user=get_user_data())

#---------------------------------------Edit Best Practice----------------------------#

@best_practice_route.route("/update_info_best_practice/<id>", methods=["GET", "POST"])
def update_best_practice(id):
        best_practice_request = BestPracticeRequest(
            db_version=request.form.get("db_version"),
            parameter=request.form.get("parameter"),
            param_default_value=request.form.get("param_default_value"),
            param_recommend_value=request.form.get("param_recommend_value"),
            for_rac_only=request.form.get("for_rac_only"),
            notes=request.form.get("notes")
        )
        response = update_best_practice_action(id, best_practice_request)
       
        if response.status_code == 200:
            return redirect(url_for("admin_route.best_practice_route.best_practice_management"))
        else:
            best_practice = get_best_practice_by_id(id)
            return render_template("detail_best_practice.html", best_practice=best_practice, user=get_user_data(), error=f"Lỗi khi cập nhật best practice: {response.text}")
