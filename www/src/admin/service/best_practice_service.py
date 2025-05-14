from core.request import RequestHandler
from admin.model.response.best_practice_response import BestPracticeResponse
from admin.model.request.best_practice_request import BestPracticeRequest 
    
# Lấy danh sách tất cả Best Practices
def get_best_practices():
    response = RequestHandler.post("/best-practice/get-all", headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        best_practices = [BestPracticeResponse(**item) for item in response.json()]
        return best_practices
    return []


# Lấy Best Practice theo ID
def get_best_practice_by_id(id):
    response = RequestHandler.get(f"/best-practice/show/{id}", headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        data = response.json()
        return data[0]
    return []


# Thêm mới một Best Practice
def add_best_practice_action(best_practice_request: BestPracticeRequest):
    data = best_practice_request.dict()
    response = RequestHandler.post(f"/best-practice/add", data=data, headers={"Content-Type": "application/json"})
    return response


# Cập nhật Best Practice theo ID
def update_best_practice_action(id, best_practice_request: BestPracticeRequest):
    data = best_practice_request.dict()
    response = RequestHandler.put(f"/best-practice/update/{id}", data=data, headers={"Content-Type": "application/json"})
    return response