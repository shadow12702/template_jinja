import pandas as pd
from flask import Blueprint, json, render_template, request
from pathlib import Path
from apps.service import chart_service
from apps.model.response.chart_response import ChartResponse
from components import echart as ec

template_path = Path(__file__).parent.parent / "templates"
echart_route = Blueprint('echart', __name__, template_folder=template_path)

# Echarts

@echart_route.route("/<chart_id>", methods=['POST', 'GET'])
def show_echart(chart_id):
    ''' show echart chart '''
    try:
        _database = json.loads(request.form.get('database'))
        _type ,_endpoint = request.form.get('chart', ''), request.form.get('link', '')
        chart_response = chart_service.get_chart_data(_endpoint, _type ,_database.get('customer_code',''), _database.get('dbid',0))
        if chart_response.status_code == 200:
            ds_json = chart_response.json()
            if ds_json:
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
            else:
                return render_template("error.html")
        
    except Exception as e:
        return render_template("error.html", title=f"Error{e}")
