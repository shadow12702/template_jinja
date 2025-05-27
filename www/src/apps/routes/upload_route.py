import os
from flask import Blueprint, render_template, request, send_file, abort
from pathlib import Path
from flask import current_app
from werkzeug.utils import secure_filename

template_path = Path(__file__).parent.parent / "templates"
upload_route = Blueprint('upload', __name__, template_folder=template_path)

@upload_route.route("/", methods=['POST', 'GET'])
def success():
    if request.method == 'POST':  
        f = request.files['file']
        filename = secure_filename(f.filename)
        
        static_path = current_app.static_folder
        upload_dir = os.path.join(static_path, "uploads")
        
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        file_path = os.path.join(upload_dir, filename)
        f.save(file_path)
        
        # Lấy tất cả file sau khi upload
        files = [f for f in os.listdir(upload_dir) 
                if os.path.isfile(os.path.join(upload_dir, f))]
        
        return render_template("upload.html", name=filename, files=files, success=True)
    
    # GET request - hiển thị tất cả file có sẵn
    static_path = current_app.static_folder
    upload_dir = os.path.join(static_path, "uploads")
    
    files = []
    if os.path.exists(upload_dir):
        files = [f for f in os.listdir(upload_dir) 
                if os.path.isfile(os.path.join(upload_dir, f))]
    
    return render_template("upload.html", files=files)

@upload_route.route("/download/<filename>")
def download_file(filename):
    try:
        filename = secure_filename(filename)
        static_path = current_app.static_folder
        upload_dir = os.path.join(static_path, "uploads")
        file_path = os.path.join(upload_dir, filename)
        
        if not os.path.exists(file_path):
            abort(404)
        
        return send_file(file_path, as_attachment=True, download_name=filename)
    except Exception as e:
        abort(404)