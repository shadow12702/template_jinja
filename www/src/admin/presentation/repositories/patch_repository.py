from admin.models.request.patch.patch_update_request import PatchUpdateRequest
from src.admin.models.model_response import PatchResponse
from src.admin.models.model_request import PatchRequest
from src.core.request import RequestHandler

class PatchRepository :
    
    
    # Hàm gọi API để lấy danh sách patch
    def get_patches():
        response = RequestHandler.post("/patch/get-patch", headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            patches = [PatchResponse(**item) for item in response.json()]
            return patches
        return []


    # Hàm gọi API để lấy thông tin một patch theo ID
    def get_patch_by_id(patch_id):
        response = RequestHandler.post("/patch/get-patch", data={"id": patch_id}, headers={"Content-Type": "application/json"})
        if response.status_code == 200 and response.json():
            for item in response.json():
                if item.get("id") == patch_id:
                    return PatchResponse(**item)
        return None


    # Hàm gọi API để thêm patch
    def update_patch_action(patch_id, patch_request: PatchRequest):
        data = {
            "root": patch_request.root,
            "db_version": patch_request.db_version,
            "type": patch_request.type,
            "format": patch_request.format,
            "patch_type": patch_request.patch_type,
            "fixed_in_ru": patch_request.fixed_in_ru,
            "fixed_in_mrp": patch_request.fixed_in_mrp,
            "description": patch_request.description,
        }
        response = RequestHandler.put(f"/patch/update/{patch_id}",data=data,headers={"Content-Type": "application/json"}
        )
        return response


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