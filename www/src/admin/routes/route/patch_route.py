from flask import Blueprint, render_template, request, redirect, session, url_for
from src.admin.models.model_response import PatchResponse
from src.admin.models.model_request import PatchRequest
from src.apps.models.responses.user_model import UserModel
from src.core.request import RequestHandler
import os

# Thiết lập thư mục template
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'templates', 'patches')

patch_route = Blueprint('patch_route', __name__, template_folder=template_dir)

# Hàm lấy dữ liệu người dùng từ session
def get_user_data():
    user_data = session.get('user')
    user = UserModel(**user_data) if user_data else None
    return user

# Hàm gọi API để lấy danh sách patch
def get_patches():
    response = RequestHandler.post("/patch/get-patch", headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        patches = [PatchResponse(**item) for item in response.json()]
        return patches
    return []

# Hàm gọi API để thêm patch
def add_patch_action(patch_request: PatchRequest):
    data = patch_request.dict()
    response = RequestHandler.post("/patch/add", data=data, headers={"Content-Type": "application/json"})
    return response

# Hàm gọi API để cập nhật patch
def edit_patch_action(patch_request: PatchRequest):
    data = patch_request.dict()
    response = RequestHandler.post("/patch/update", data=data, headers={"Content-Type": "application/json"})
    return response

# Route chính quản lý patch
@patch_route.route("/db-patch")
def patches_management():
    patches = get_patches()
    return render_template("patches_management.html", patches=patches, user=get_user_data())

# Route hiển thị form thêm patch
@patch_route.route("/add_patch")
def add_patch():
    return render_template("add_patches.html", user=get_user_data())

# Route xử lý thêm patch
@patch_route.route("/add_new_patch", methods=["GET", "POST"])
def add_new_patch():
    if request.method == "POST":
        form = request.form

        patch_request = PatchRequest(
            id=int(form.get("id", 0)),
            root=int(form.get("root", 0)),
            db_version=form.get("db_version", ""),
            type=form.get("type", ""),
            format=form.get("format", ""),
            patch_type=form.get("patch_type", ""),
            fixed_in_ru=form.get("fixed_in_ru", ""),
            fixed_in_mrp=form.get("fixed_in_mrp", "NOT APPLICABLE"),
            description=form.get("description", "")
        )

        # Kiểm tra các trường bắt buộc
        required_fields = {
            "db_version": patch_request.db_version,
            "type": patch_request.type,
            "format": patch_request.format,
            "patch_type": patch_request.patch_type,
            "fixed_in_ru": patch_request.fixed_in_ru,
            "description": patch_request.description
        }

        empty_fields = [field for field, value in required_fields.items() if not value]
        if empty_fields:
            error = f"Vui lòng điền đầy đủ các trường: {', '.join(empty_fields)}"
            return render_template("add_patches.html", user=get_user_data(), error=error)

        response = add_patch_action(patch_request)

        if response.status_code == 200:
            return redirect(url_for("admin_route.patch_route.patches_management"))
        else:
            return render_template("add_patches.html", user=get_user_data(), error=f"Lỗi khi thêm patch: {response.text}")

    return render_template("add_patches.html", user=get_user_data())
