from admin.models.response.awr_repo_info_response import AwrRepoInfoResponse
from core.request import RequestHandler

class AwrRepository:
    
    
    # Lấy danh sách khách hàng
    def get_db_repo_info():
        response = RequestHandler.post("/awr/get-awr-repo-info", headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            return [AwrRepoInfoResponse(**item) for item in response.json()]
        return []