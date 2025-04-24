from flask import Blueprint, redirect, render_template, session, url_for
from admin.presentation.repository import AwrRepository
import os

# Tính toán đường dẫn chính xác đến thư mục chứa test.html
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'templates', 'awr_database')

awr_route = Blueprint('awr_route', __name__, template_folder=template_dir)

#---------------------------------------Get all Awr---------------------------#
@awr_route.route("/awr-db")
def awr():
    db_repo_info = [] 
    try:
        # Lấy thông tin repo db
        db_repo_info = AwrRepository.get_db_repo_info()
        return render_template("awr_database.html" , db_repo_info = db_repo_info)
    
    except Exception as ex:
        print(f"Lỗi trong route awr: {ex}")
        raise ex