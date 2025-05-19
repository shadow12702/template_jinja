# app/service/chart_service.py

from core.request import RequestHandler

def get_chart_data(endpoint:str , type, customer_code: str, dbid: int):
    """
    Get chart data from the server.
    """
    data_request = {
        "metric_type" : type,
        "customer_code": customer_code,
        "dbid": dbid
    }
    return  RequestHandler.post(endpoint, 
                                data=data_request, 
                                headers={"Content-Type": "application/json"})
    


