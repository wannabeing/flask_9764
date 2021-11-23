import json

import unicodedata
from flask import Blueprint, render_template, request, url_for
from views.login_views import login_required
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename
import ocr
import re
from unicodedata import normalize
import os

bp = Blueprint('ocr', __name__, url_prefix='/ocr')
appkey = 'f26d1496764a6965cdd632f3d5da106a'


@bp.route('/main/')
@login_required
def main_page():
    return render_template('ocr/ocr_main.html')


@bp.route('/check/', methods=['POST', 'GET'])
@login_required
def print():
    if request.method == 'POST':
        file = request.files["file"]
        path = 'C:/projects/blogproject/static/ocr_img/' + file.filename
        file.save('./static/ocr_img/'+secure_filename(file.filename))

        # dumps()는 Python객체(dict)를 JSON문자열로 변환 / lodas는 그 반대
        ocr_result = ocr.kakao_ocr(path, appkey).json()
        dumps = json.dumps(ocr_result, ensure_ascii=False, sort_keys=True)
        loads = json.loads(dumps)

        print = []
        for i in range(len(ocr_result['result'])):
            print.append(ocr_result['result'][i]['recognition_words'][0])
        str = '\n'.join(print)
        kind = ''
        if re.match(r'(자동차)', str) != None:
            msg = str
            kind = "운전면허증"
        elif re.match(r'(주민)', str) != None:
            msg = str
            kind = "주민등록증"
        else:
            msg = str
            kind = None
        return render_template('ocr/ocr_print.html', ocr=msg, kind=kind, name=file.filename)