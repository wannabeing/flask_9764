import json

from flask import Blueprint, render_template, request, url_for, session, flash
from views.login_views import login_required
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash,check_password_hash

from blog import db
from models import User

import ocr
import re

bp = Blueprint('ocr', __name__, url_prefix='/ocr')
appkey = 'f26d1496764a6965cdd632f3d5da106a'


@bp.route('/main/')
@login_required
def main_page():
    return render_template('ocr/ocr_main.html')


@bp.route('/print/', methods=['POST', 'GET'])
@login_required
def print():
    if request.method == 'POST':
        file = request.files["file"] # name=file, input=file 가져오기
        path = 'C:/projects/blogproject/static/ocr_img/' + file.filename
        file.save('./static/ocr_img/'+secure_filename(file.filename))

        # dumps()는 Python객체(dict)를 JSON문자열로 변환 / lodas는 그 반대
        ocr_result = ocr.kakao_ocr(path, appkey).json()
        # dumps = json.dumps(ocr_result, ensure_ascii=False)
        # loads = json.loads(dumps)

        ocr_array = []
        for i in range(len(ocr_result['result'])):
            ocr_array.append(ocr_result['result'][i]['recognition_words'][0])
        ocr_str = ''.join(ocr_array)
        ocr_str = ocr_str.replace(' ', '')

        # 운전면허증/주민등록증 구분하여 html에 kind로 넘기고, msg에 ocr로 변환한 변수 값(str)을 넘긴다.
        if re.search(r'(자동차)', ocr_str) != None:
            ocr_msg = ocr_str
            ocr_kind = "운전면허증"
            joo = getJoomin(ocr_msg)  # 함수를 써서 간략히 표현해봄
            fir_joo = joo.split('-')[0]
            sec_joo = joo.split('-')[1]
        elif re.search(r'(주민)', ocr_str) != None:
            ocr_msg = ocr_str
            ocr_kind = "주민등록증"
            joo = getJoomin(ocr_msg)   # 함수를 써서 간략히 표현해봄
            fir_joo = joo.split('-')[0]
            sec_joo = joo.split('-')[1]
            text = '9801091157119'
            out = jooValidation(text)
        else:
            ocr_msg = ocr_str
            ocr_kind = None
            joo = getJoomin(ocr_msg)  # 함수를 써서 간략히 표현해봄
            fir_joo = joo.split('-')[0]
            sec_joo = joo.split('-')[1]
        return render_template('ocr/ocr_print.html', ocr=out, kind=ocr_kind,
                               name=file.filename, path=path, fir_joo=fir_joo, sec_joo=sec_joo)


@bp.route('/check/', methods=['POST', 'GET'])
@login_required
def check():
    if request.method == 'POST':

        username = request.form["username"]  # form에서 name='username' 가져오기
        password = request.form["password"]  # form에서 name='password' 가져오기
        fir_joo = request.form["fir_joo"]    # form에서 name='fir_joo' 가져오기
        sec_joo = request.form["sec_joo"]    # form에서 name='sec_joo' 가져오기


        # form에서 name='username'과 같은 username인 User의 DB 가져오기
        user = User.query.filter_by(username=username).first()

        # 여기 고쳐야 댐
        if user:
            if check_password_hash(user.password, password):
                user.fir_joo = fir_joo
                user.sec_joo = sec_joo
                db.session.commit()
            else:
                flash('비밀번호가 틀립니다.')
        else:
            flash('존재하지 않는 사용자입니다.')
        return render_template('ocr/ocr_check.html', username=username, name=user.name,
                               fir_joo=fir_joo, sec_joo=sec_joo)


# 정규표현식으로 주민등록번호 부분 추출해서 return 값으로 넘기는 함수
def getJoomin(joomin):
    joo = re.search('r(\d{7,13)|(\d{4,6}-\d{5,7})', joomin)[0]
    return joo

def jooValidation(joomin):
    total = 0
    weight = [2,3,4,5,6,7,8,9,2,3,4,5]
    for i in range(12):
        multi = int(joomin[i])*(i%8+2)
        total += multi
        total = (11-total%11) %10
        if int(joomin[12]==total):
            return 'True'
        else:
            return 'False'