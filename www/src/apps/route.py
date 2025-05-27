# apps/route.py

from flask import Blueprint, render_template, request, redirect, url_for
from pathlib import Path

from apps.routes.chart_route import echart_route
from apps.routes.upload_route import upload_route


template_path = Path(__file__).resolve().parents[0] / 'templates'
app_route = Blueprint('apps', __name__, template_folder=template_path)

app_route.register_blueprint(echart_route, url_prefix='/echarts')
app_route.register_blueprint(upload_route, url_prefix='/upload')

@app_route.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

