# admin/routes/awr_repo_route.py

from flask import Blueprint, render_template, request, redirect, url_for
from base.service import awr_repo_service

from pathlib import Path
template_path = Path(__file__).resolve().parents[1] / 'templates/awr_repo'
awr_repo_route = Blueprint('awr_repo', __name__, template_folder=template_path)

@awr_repo_route.route('/list')
def list_awrs():
    '''Get all awrs.'''
    _list = awr_repo_service.get_awr_repo()
    return render_template('awr_repo.html', awr_repo=_list)

