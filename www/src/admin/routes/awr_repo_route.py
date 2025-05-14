# admin/routes/awr_repo_route.py

from flask import Blueprint, jsonify, render_template, request
from base.service import awr_repo_service

from pathlib import Path
template_path = Path(__file__).resolve().parents[1] / 'templates/awr_repo'
awr_repo_route = Blueprint('awr_repo', __name__, template_folder=template_path)

@awr_repo_route.route('/list')
def list_awrs():
    '''Get all awrs.'''
    _list = awr_repo_service.get_awr_repo()
    return render_template('awr_repo.html', awr_repo=_list)


@awr_repo_route.route('/get-awr-data', methods=['POST'])
def get_awr_data_by_customer():
    try:
        data = request.get_json()
        customer_code = data.get('customer_code')
        if not customer_code:
            return jsonify({'error': 'Customer code is rerquired'}), 400
        
        databases = awr_repo_service.get_awr_repo_by_customer(customer_code)
        if databases:
            return jsonify([{'database': db.model_dump()} for db in databases])
        return jsonify([])
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500
