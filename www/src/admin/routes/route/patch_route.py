from flask import Blueprint, render_template, session, request, redirect, url_for
from src.admin.models.model_response import PatchResponse
from src.admin.presentation.service import ApiService
from src.apps.models.responses.user_model import UserModel
from src.core.request import RequestHandler
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'templates', 'patches')

patch_route = Blueprint('patch_route', __name__, template_folder=template_dir)

def get_patches():
    response = RequestHandler.post("/patch/get-patch", headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        patches = response.json() or []
        return patches
    return []

def get_user_data():
    user_data = session.get('user')
    user = UserModel(**user_data) if user_data else None
    return user

@patch_route.route("/patch")
def patches_management():
    user = get_user_data()
    menu = ApiService.get_menu(1)
    
    try:
        patches = get_patches()
    except Exception as e:
        print(f"Error fetching patches: {e}")
        patches = []

    return render_template('patches_management.html', 
                          user=user, 
                          menu=menu, 
                          patches=patches)

def add_patch_action(DbVersion: str, Type: str, Format: str, PatchRoot: int, PatchID: int, PatchType: str, FixedInRU: str, FixedInMRP: str, Description: str):
    data = {
        "DbVersion": DbVersion,
        "Type": Type,
        "Format": Format,
        "PatchRoot": PatchRoot,
        "PatchID": PatchID,
        "PatchType": PatchType,
        "FixedInRU": FixedInRU,
        "FixedInMRP": FixedInMRP,
        "Description": Description
    }
    response = RequestHandler.post("/patch/add", data=data, headers={"Content-Type": "application/json"})
    return response

@patch_route.route("/add_new_patch", methods=["GET", "POST"])
def add_new_patch():
    if request.method == "POST":
        DbVersion = request.form.get("DbVersion", "").strip() 
        Type = request.form.get("Type", "").strip()
        Format = request.form.get("Format", "").strip()
        PatchRoot = int(request.form.get("PatchRoot", 0))
        PatchID = int(request.form.get("PatchID", 0))
        PatchType = request.form.get("PatchType", "").strip()
        FixedInRU = request.form.get("FixedInRU", "").strip()
        FixedInMRP = request.form.get("FixedInMRP", "NOT APPLICABLE").strip()
        Description = request.form.get("Description", "").strip()

        required_fields = {
            "DbVersion": DbVersion,
            "Type": Type,
            "Format": Format,
            "PatchType": PatchType,
            "FixedInRU": FixedInRU,
            "FixedInMRP": FixedInMRP,
            "Description": Description
        }
        
        empty_fields = [field for field, value in required_fields.items() if not value]
        if empty_fields:
            error = f"Vui lòng điền đầy đủ các trường: {', '.join(empty_fields)}"
            return render_template("add_patches.html", user=get_user_data(), error=error)

        response = add_patch_action(DbVersion, Type, Format, PatchRoot, PatchID, PatchType, FixedInRU, FixedInMRP, Description)

        if response.status_code == 200:
            return redirect(url_for("admin_route.patch_route.patches_management"))
        else:
            return render_template("add_patches.html", user=get_user_data(), error=f"Lỗi khi thêm patch: {response.text}")

    return render_template("add_patches.html", user=get_user_data())

def edit_patch_action(DbVersion: str, Type: str, Format: str, PatchRoot: int, PatchID: int, PatchType: str, FixedInRU: str, FixedInMRP: str, Description: str):
    data = {
        "DbVersion": DbVersion,
        "Type": Type,
        "Format": Format,
        "PatchRoot": PatchRoot,
        "PatchID": PatchID,
        "PatchType": PatchType,
        "FixedInRU": FixedInRU,
        "FixedInMRP": FixedInMRP,
        "Description": Description
    }
    response = RequestHandler.post("/patch/update", data=data, headers={"Content-Type": "application/json"})
    return response

