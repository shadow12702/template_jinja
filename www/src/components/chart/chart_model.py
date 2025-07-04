from typing import List
from pydantic import BaseModel

class ChartSize(BaseModel):
    width: int = 600
    height: int = 300

class ChartModel(BaseModel):
    id: str
    type: str 
    title: str
    x_axis: List[str]
    y_axis: List[str]
    show_title: bool = True
    show_legend: bool = True
    show_grid: bool = True
    size: ChartSize = ChartSize(width=600, height=300)
    