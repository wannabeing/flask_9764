from blog import *
from flask import Blueprint, request, send_file
from werkzeug.utils import secure_filename
from views.login_views import login_required
import os

bp = Blueprint("files", __name__, url_prefix='/files')


# 메인 HTML 렌더링
@bp.route('/main/')
@login_required
def main_page():
    return render_template('ftp/ftp_main.html')


# 업로드 HTML 렌더링
@login_required
@bp.route('/upload/')
def upload_page():
    return render_template('ftp/ftp_upload.html')


# 파일 업로드 처리
@bp.route('/uploadcheck/', methods =['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['file'] # POST 방식으로 업로드페이지에서 넘어오면 file이라는 이름의 폼으로 전송된 파일을 가져옴
        file.save('./uploads/'+secure_filename(file.filename)) # 파일이름을 보호하고 file.save로 파일 객체를 지정한 폴더에 저장한다
        file_list = os.listdir("./uploads")
        return render_template('ftp/ftp_check.html', file_list=file_list)


# 다운로드 HTML 렌더링
@bp.route('/download/')
@login_required
def down_page():
    file_list = os.listdir("./uploads")
    return render_template('ftp/ftp_download.html', file_list=file_list)


# 파일 다운로드 처리
@bp.route('/fileDownload/', methods = ['GET', 'POST'])
@login_required
def down_file():
    if request.method == 'POST':
        sw = 0
        file_list = os.listdir("./uploads")
        for x in file_list:
            if(x==request.form['file']):
                sw = 1
        path = "./uploads/"
        return send_file(path + request.form['file'],
                         attachment_filename=request.form['file'],
                         as_attachment=True)


# 파일 리스트 HTML 렌더링
@bp.route('/list/')
@login_required
def list_page():
    file_list = os.listdir("./uploads")
    return render_template('ftp/ftp_list.html', file_list=file_list)