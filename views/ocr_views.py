import json
import os.path

from flask import Blueprint, render_template, request, url_for, session, flash, g, jsonify


from views.login_views import login_required
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from blog import db
from models import User

import ocr
import re

bp = Blueprint('ocr', __name__, url_prefix='/ocr')
appkey = 'f26d1496764a6965cdd632f3d5da106a'  # OCR 을 위한 API Key


@bp.route('/main/')
@login_required
def main_page():
    return render_template('ocr/ocr_main.html')

@bp.route('/error/')
@login_required
def error():
    return render_template('ocr/ocr_error.html')


@bp.route('/print/', methods=['POST', 'GET'])
@login_required
def print():
    if request.method == 'POST':
        user = User.query.filter_by(username=g.user.username).first()

        if request.get_json():  # 비동기 통신의 경우
            result = request.get_json()  # 비동기 통신 데이터 저장

            if result['kind'] == 'password':  # 데이터의 종류가 password 일 경우
                password = result['password']
                if check_password_hash(user.password, password):  # 입력받은 pw와 기존 user.pw 비교
                    return jsonify(result="success", data=result)
                else:
                    return jsonify(result="error", data=result), 500

            elif result['kind'] == 'joo':  # 데이터의 종류가 joo 일 경우
                return jsonify(result="success", data=result)

            elif result['kind'] == 'submit':  # 데이터의 종류가 submit 일 경우
                user.fir_joo = result['fir_joo']
                user.sec_joo = result['sec_joo']
                db.session.commit()
                return jsonify()

            else:
                return jsonify(result="error"), 500

        else:  # main 에서 넘어온 POST 의 경우 (이미지 제출시)
            file = request.files["file"]  # name=file, input=file 가져오기
            file.save('./static/ocr_img/' + secure_filename(file.filename))
            path = os.getcwd() + "/static/ocr_img/" + file.filename

            try:
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

                match = re.match(r'(주민)', ocr_str)[0]

                if re.search(r'(운전)', ocr_str):
                    ocr_msg = ocr_str
                    ocr_kind = "운전면허증"
                    joo = re.search('r(\d{7,13})|(\d{4,6}-\d{5,7})', ocr_msg)[0]
                    fir_joo = joo.split('-')[0]
                    sec_joo = joo.split('-')[1]
                elif re.search(r'(주민)', ocr_str):
                    # if ocr_str:
                    #     ocr_str = re.search('r(\d{7,13)|(\d{4,6}-\d{5,7})', ocr_str)[0]
                    #     return render_template('ocr/ocr_error.html', test=ocr_str)
                    ocr_msg = ocr_str
                    ocr_kind = "주민등록증"
                    joo = re.search('r(\d{7,13})|(\d{4,6}-\d{5,7})', ocr_msg)[0]
                    fir_joo = joo.split('-')[0]
                    sec_joo = joo.split('-')[1]
                # 운전/주민 둘 다 없으면 공백으로 넘김
                else:
                    return render_template('ocr/ocr_print.html', kind='', g_user=g.user.username,
                                           name=file.filename, fir_joo='', sec_joo='')

                return render_template('ocr/ocr_print.html', kind=ocr_kind, g_user=g.user.username,
                                       name=file.filename, fir_joo=fir_joo, sec_joo=sec_joo)
            # 이미지 반환 중 오류발생 시
            except Exception as e:
                return render_template('ocr/ocr_print.html', kind='', g_user=g.user.username,
                                       name=file.filename, fir_joo='', sec_joo='')
    return render_template('ocr/ocr_print.html', kind='', g_user=g.user.username,
                           name='', fir_joo='', sec_joo='')


@bp.route('/check/', methods=['POST', 'GET'])
@login_required
def check():
    user = User.query.filter_by(username=g.user.username).first()
    return render_template('ocr/ocr_check.html', username=user.username, name=user.name,
                           fir_joo=user.fir_joo, sec_joo=user.sec_joo)


# 정규표현식으로 주민등록번호 부분 추출해서 return 값으로 넘기는 함수
def getJoomin(joomin):
    joo = re.search('r(\d{7,13)|(\d{4,6}-\d{5,7})', joomin)[0]
    return joo