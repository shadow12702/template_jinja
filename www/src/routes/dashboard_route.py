import pandas as pd
from flask import Blueprint, render_template
from sample.fake_data import FakeData
from components.chart import plotlies as pl
from components.chart import echarts as ec

db_route = Blueprint('db_route', __name__)

@db_route.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
    

@db_route.route("/plotly/line/<chart_id>")
def show_plotly_chart(chart_id):
    df = FakeData.generate_data()
    # ['Date', 'Item', 'City', 'Cost', 'Revenue']
    chart_model = pl.ChartModel(id=chart_id, type='line', title="Line Chart", x_axis="Date", y_axis=["Cost", "Revenue"])
    line = pl.LineChart(chart_model, df)
    html = line.render()
    return render_template("charts/line.html", graph_html=html, title=line.chart_model.title)

@db_route.route("/plotly/area-line")
def show_area_chart():
    df = FakeData.generate_data()   
    chart_model = pl.ChartModel(id="area-line", type='area', title="Area Chart", x_axis="City", y_axis=["Cost", "Revenue"])
    chart = pl.AreaLineChart(chart_model, df)
    html = chart.render(stacked=True)
    return render_template("charts/area_line.html", graph_html=html, title=chart.chart_model.title)

@db_route.route("/plotly/pie")
def show_plotly_pie_chart():
    df = FakeData.generate_data()
    chart_model = pl.ChartModel(id="pie", type='pie', title="Pie Chart", x_axis="City", y_axis=["Cost"])
    chart = pl.PieChart(chart_model, df)
    html = chart.render()
    return render_template("charts/pie.html", graph_html=html, title=chart.chart_model.title)

@db_route.route("/plotly/bar")
def show_plotly_bar_chart():
    df = FakeData.generate_data()
    chart_model = pl.ChartModel(id="bar", type='bar', title="Bar Chart", x_axis="Item", y_axis=["Cost", "Revenue"])
    chart = pl.BarChart(chart_model, df)
    html = chart.render(stacked=True, horizontal=False)
    return render_template("charts/bar.html", graph_html=html, title=chart.chart_model.title)

# Echarts

@db_route.route("/echart/line/<chart_id>")
def show_echart_chart(chart_id):
    df = FakeData.generate_data()
    # ['Date', 'Item', 'City', 'Cost', 'Revenue']
    if chart_id == "1":
        chart_model = ec.ChartModel(id=chart_id, type='line', title=f"Line Chart {chart_id}", x_axis="Date", y_axis=["Cost", "Revenue"])
        chart = ec.LineChart(chart_model, df)
        html = chart.render(horizontal=False, show_label=False)
    elif chart_id =="2":
        chart_model = ec.ChartModel(id=chart_id, type='line', title=f"Line Chart {chart_id}", x_axis="City", y_axis=["Revenue"])
        chart = ec.BarChart(chart_model, df)
        html = chart.render(horizontal=False, show_label=False)
    else:
        chart_model = ec.ChartModel(id=chart_id, type='pie', title=f" Chart {chart_id}", x_axis="Item", y_axis=["Cost"])
        chart = ec.PieChart(chart_model, df)
        html = chart.render(donut=True)

    return render_template("charts/line.html", graph_html=html, title=chart.chart_model.title)

@db_route.route("/echart/pie")
def show_echart_pie_chart():
    df = FakeData.generate_data()
    chart_model = ec.ChartModel(id="pie", type='pie', title="Pie Chart", x_axis="City", y_axis=["Cost"])
    chart = ec.PieChart(chart_model, df)
    html = chart.render(donut=True)
    return render_template("charts/pie.html", graph_html=html, title=chart.chart_model.title)
@db_route.route("/echart/bar")
def show_echart_bar_chart():
    df = FakeData.generate_data()
    chart_model = ec.ChartModel(id="bar", type='bar', title="Bar Chart", x_axis="Item", y_axis=["Cost", "Revenue"])
    chart = ec.BarChart(chart_model, df)
    html = chart.render(stacked=False, horizontal=False)
    return render_template("charts/bar.html", graph_html=html, title=chart.chart_model.title)

