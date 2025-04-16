import pandas as pd
from flask import Blueprint, render_template
from core.request import RequestHandler

from sample.fake_data import FakeData
from components.chart import plotlies as pl
from components.chart import echarts as ec
from src.apps.models.responses.chart_response import ChartResponse

chart_route = Blueprint('chart_route', __name__)


# Echarts

@chart_route.route("/chart-route/<chart_id>")
def show_echart_chart( chart_id):
    # Lấy dữ liệu menu
    chart_response = RequestHandler.post("/cdb/get-ash-overall-wait-class", 
                                    data={
                                        "customer_code": "ACB01",
                                        "dbid": 3118345579
                                    }, 
                                    headers={"Content-Type": "application/json"})
    
    if chart_response.status_code == 200:
        ds_json = chart_response.json()
        ds_json["chart_model"]["id"] = chart_id 
        chart_info = ChartResponse(**ds_json) 
        chart_model = ec.ChartModel(id=chart_id, type=chart_info.chart_model.type, title=chart_info.chart_model.title, x_axis=chart_info.chart_model.x_axis, y_axis=chart_info.chart_model.y_axis)
        df = pd.DataFrame(chart_info.data)

        if chart_info.chart_model.type == "line":
            chart = ec.LineChart(chart_model, df)
            html = chart.render(horizontal=False, show_label=False)
        elif chart_info.chart_model.type =="bar":
            chart = ec.BarChart(chart_model, df)
            html = chart.render(horizontal=False, show_label=False)
        else: 
            chart = ec.PieChart(chart_model, df)
            html = chart.render(donut=True)
            
    return render_template("chart_detail.html", graph_html=html, title=chart.chart_model.title)
