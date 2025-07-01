from flask import Blueprint, render_template, request, redirect, url_for
from pathlib import Path
from admin.model.request.chart_model_request import ChartModelRequest
from admin.service import chart_model_service
from admin.service.chart_model_service import delete_model_chart, get_chart_model_by_id
template_path = Path(__file__).resolve().parents[1] / 'templates/chart_model'
chart_model_route = Blueprint('chart_model', __name__, template_folder=template_path)

@chart_model_route.route('/list')
def list_chart_models():
    '''Get all chart models.'''
    _list = chart_model_service.get_all_chart_models()
    return render_template('chart_model.html', chart_models=_list)


@chart_model_route.route('/delete/<id>', methods=['GET','POST'])
def delete_chart_model(id):
    chart_model = delete_model_chart(id)
    if chart_model:
        return redirect(url_for('base.admin.chart_model.list_chart_models'))
    else:
        return redirect(url_for('base.admin.chart_model.list_chart_models'))
    



@chart_model_route.route("/detail/<id>")
# -Detail Chart Model
def detail_chart_model(id):
    chart_model = chart_model_service.get_chart_model_by_id(id)
    return render_template("detail_chart_model.html", chart_model=chart_model)


@chart_model_route.route("/update_chart_model/<id>", methods=["GET", "POST"])
#Edit Chart Model
def update_chart_model(id):
    _update_chart_model = ChartModelRequest(**request.form)
    response = chart_model_service.update_chart_model(id, _update_chart_model)
    if response.status_code == 200:
        return redirect(url_for("base.admin.chart_model.list_chart_models"))
    else:
        chart_model = chart_model_service.get_chart_model_by_id(id)
        return render_template("detail_chart_model.html", chart_model=chart_model,error=f"Lỗi khi cập nhật chart model: {response.text}")
    


@chart_model_route.route('/add')
def add():
    '''Prompt to add a new chart model.'''
    return render_template('add_chart_model.html')

@chart_model_route.route('/add_chart_model', methods=['POST'])
def add_chart_model():
    '''Add a new chart model.'''
    if request.method == 'POST':
        _new_chart_model = ChartModelRequest(**request.form)
        response = chart_model_service.add_chart_model(_new_chart_model)
        if response.status_code == 200:
            return redirect(url_for('base.admin.chart_model.list_chart_models'))
        else:
            error_message = response.json().get('message', 'Failed to add chart model')
            return render_template('add_chart_model.html', error=error_message)
    return render_template('add_chart_model.html')