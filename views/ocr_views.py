import os.path
from flask import Blueprint, render_template, request, url_for
from views.login_views import login_required
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename
import ocr

bp = Blueprint('ocr', __name__, url_prefix='/ocr')
appkey = 'f26d1496764a6965cdd632f3d5da106a'


@bp.route('/main/')
@login_required
def main_page():
    return render_template('ocr/ocr_main.html')


@bp.route('/check/', methods=['POST', 'GET'])
@login_required
def check():
    if request.method == 'POST':
        file = request.files["file"]
        file.save('./static/ocr_img/'+secure_filename(file.filename))
        path = 'C:/projects/blogproject/static/ocr_img/'+file.filename
        output = ocr.kakao_ocr(path, appkey).json()
        return render_template('ocr/ocr_check.html', real=output)

@bp.route('/test/')
@login_required
def test():
    path = 'C:/projects/blogproject/static/ocr_img/hdg_2.jpg'
    resize = ocr.kakao_ocr_resize(path)
    if resize is not None:
        path = resize

    output = ocr.kakao_ocr(path, appkey).json()
    return render_template('ocr/ocr_test.html', real=output)