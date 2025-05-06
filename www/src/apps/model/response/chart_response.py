

from pydantic import BaseModel

from components.chart.chart_model import ChartModel


class ChartResponse(BaseModel):
    chart_model: ChartModel
    data: list
