import os.path

from flask import Blueprint, render_template, request, url_for
from views.login_views import login_required
from werkzeug.utils import redirect

import ocr

bp = Blueprint('ocr', __name__, url_prefix='/ocr')
appkey = 'f26d1496764a6965cdd632f3d5da106a'


@bp.route('/main/')
@login_required
def main_page():
    return render_template('ocr/ocr_main.html')


@bp.route('/check/')
@login_required
def check():
    path ='C:/projects/blogproject'+ url_for('static', filename='ocr_images/hdg.jpg')
    resize = ocr.kakao_ocr_resize(path)
    if resize is not None:
        path = resize
    output = ocr.kakao_ocr(path, appkey).json()
    return render_template('ocr/ocr_check.html', real=output)