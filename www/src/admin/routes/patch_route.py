from flask import Blueprint, render_template, request, redirect, session, url_for
from admin.model.request.patch_request import PatchRequest
from admin.service import patch_service
from pathlib import Path

template_path = Path(__file__).resolve().parents[1] / 'templates/patch'
patch_route = Blueprint('db_patch', __name__, template_folder=template_path)

# Route chính quản lý patch
@patch_route.route("/")
def patches_management():
    _list = patch_service.get_patches()
    return render_template("patches.html", patches=_list)

# Route hiển thị form thêm patch
@patch_route.route("/add_patch")
def add_patch():
    return render_template("add_patch.html")

# Route xử lý thêm patch
@patch_route.route("/add_new_patch", methods=["GET", "POST"])
def add_new_patch():
    if request.method == "POST":
        _new_patch = PatchRequest(**request.form())
        response = patch_service.add_patch_action(_new_patch)
        if response.status_code == 200:
            return redirect(url_for("admin_route.patch_route.patches_management"))
        else:
            return render_template("add_patch.html", error=f"Lỗi khi thêm patch: {response.text}")

    return render_template("add_patch.html")
