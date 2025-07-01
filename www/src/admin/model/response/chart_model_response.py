from pydantic import BaseModel
from datetime import datetime

class ChartModelResponse(BaseModel):
    Id : int
    chart_key: str
    type: str
    title: str
    x_axis: str
    y_axis: str
    show_legend: bool = True
    show_tooltip: bool = False
    show_grid: bool = False
    show_x_axis: bool = True
    show_y_axis: bool = True
    show_x_label: bool = False
    show_y_label: bool = False