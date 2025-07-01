from admin.model.request.chart_model_request import ChartModelRequest
from admin.model.response.chart_model_response import ChartModelResponse
from core.request import RequestHandler

def get_all_chart_models():
    response = RequestHandler.post("/chart-model/get-all", headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        return [ChartModelResponse(**item) for item in response.json()]
    return []

def get_chart_model_by_id(id: str):
    """
    Get chart model information by ID.
    """
    try:
        if not id:
            raise ValueError("ID cannot be empty")
        response = RequestHandler.get(f'/chart-model/show/{id}', headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            return ChartModelResponse(**response.json())
        return None
    except Exception as e:
        raise e

def delete_model_chart(id: str):
    """
    delete model chart.
    """
    try:
        if not id:
            raise ValueError("ID cannot be empty")
        response = RequestHandler.delete(f'/chart-model/delete/{id}', headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            return response
        
        return None
    except Exception as e:
        raise e

def update_chart_model(id, chart_model_request: ChartModelRequest):
    data = chart_model_request.dict()
    response = RequestHandler.put(f"/chart-model/update/{id}", data=data, headers={"Content-Type": "application/json"})
    return response

def add_chart_model(chart_model: ChartModelRequest):
    """
    Add a new chart model.
    """
    try:
        if not chart_model:
            raise ValueError("Chart model cannot be empty")
        response = RequestHandler.post('/chart-model/add', data=chart_model.model_dump(), headers={"Content-Type": "application/json"})
        return response
    except Exception as e:
        raise e
    