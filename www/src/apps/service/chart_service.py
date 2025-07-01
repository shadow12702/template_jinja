# app/service/chart_service.py

from core.request import RequestHandler
from apps.model.request.db_request import DbRequest

def get_chart_data(endpoint:str , db_request: DbRequest, type:str=''):
    """
    Get chart data from the server.
    """
    if not endpoint:
        raise ValueError("Endpoint cannot be empty")
    if not db_request:
        raise ValueError("Database request cannot be empty")
    
    _data_request = db_request.model_dump()
    if type:
        _data_request["metric_type"] = type
    
    return  RequestHandler.post(endpoint, 
                                data=_data_request, 
                                headers={"Content-Type": "application/json"})
    