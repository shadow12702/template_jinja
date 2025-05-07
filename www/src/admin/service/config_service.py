from admin.model.response.config_response import ConfigResponse
from core.request import RequestHandler

def get_all_configs():
    response = RequestHandler.post("/config/get-all", headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        return [ConfigResponse(**item) for item in response.json()]
    return []

def get_config_by_type_key(type_, key):
    response = RequestHandler.get(f"/config/show/{type_}/{key}", headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        return ConfigResponse(**response.json())
    return None

def add_config_action(data):
    return RequestHandler.post("/config/add", data=data, headers={"Content-Type": "application/json"})

def update_config_action(type_, key, data):
    return RequestHandler.put(f"/config/update/{type_}/{key}", data=data, headers={"Content-Type": "application/json"})
