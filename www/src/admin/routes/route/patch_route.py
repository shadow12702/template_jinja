from flask import Blueprint, render_template, request, redirect, session, url_for
from admin.models.request.patch.patch_update_request import PatchUpdateRequest
from admin.models.request.patch.patch_request import PatchRequest
from admin.presentation.repository import PatchRepository
from src.admin.models.model_request import PatchRequest

import os

# Thiết lập thư mục template
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'templates', 'patches')
patch_route = Blueprint('patch_route', __name__, template_folder=template_dir)

# Route chính quản lý patch
@patch_route.route("/db-patch")
def patches_management():
    patches = PatchRepository.get_patches()
    return render_template("patches_management.html", patches=patches)

# Route hiển thị form thêm patch
@patch_route.route("/add_patch")
def add_patch():
    return render_template("add_patches.html")

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
            return render_template("add_patches.html", error=error)

        response = PatchRepository.add_patch_action(patch_request)

        if response.status_code == 200:
            return redirect(url_for("admin_route.patch_route.patches_management"))
        else:
            return render_template("add_patches.html", error=f"Lỗi khi thêm patch: {response.text}")

    return render_template("add_patches.html")

# Route hiển thị form chỉnh sửa patch
@patch_route.route("/edit_patch/<int:patch_id>")
def edit_patch(patch_id):
    patch = PatchRepository.get_patch_by_id(patch_id)
    if not patch:
        return render_template("edit_patches.html", error="Patch không tồn tại trong hệ thống")
    return render_template("edit_patches.html", patch=patch)

# Route xử lý cập nhật patch
@patch_route.route("/edit_patch", methods=["POST"])
def update_patch():
    if request.method == "POST":
        id=request.form.get("id")
        patch_request = PatchUpdateRequest(
            root=int(request.form.get("root")),
            db_version=request.form.get("db_version", ""),
            type=request.form.get("type", ""),
            format=request.form.get("format", ""),
            patch_type=request.form.get("patch_type", ""),
            fixed_in_ru=request.form.get("fixed_in_ru", ""),
            fixed_in_mrp=request.form.get("fixed_in_mrp", "NOT APPLICABLE"),
            description=request.form.get("description", "")
        )
        response = PatchRepository.update_patch_action( id ,patch_request)

        if response.status_code == 200:
            return redirect(url_for("admin_route.patch_route.patches_management"))
        else:
            return render_template("edit_patches.html", patch=patch_request , error=f"Lỗi khi cập nhật patch:")

    return redirect(url_for("admin_route.patch_route.edit_patch", id = id ))