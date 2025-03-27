import pandas as pd
from components.chart.chart_model import ChartModel

class Chart:
    
    def __init__(self, chart_model: ChartModel, data: pd.DataFrame):
        self.chart_model = chart_model
        self.data = data
        self.html = None

    def render(self):
        raise NotImplementedError("Need implement this method in subclass")