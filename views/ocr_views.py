import json
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
        output = ocr.kakao_ocr(path, appkey).json() #dic 구조인거 같음 (list)
        dict = output.values()
        test = output['result'][0]['recognition_words'][0]
        # outputdata는 JSON 문자열임/ dumps()는 Python객체를 JSON문자열로 변환
        outputdata = json.dumps(output, ensure_ascii=False, sort_keys=True)
        array = json.loads(outputdata)
        ex = len(array['result'])
        print = []
        for i in range(len(array['result'])):
            print.append(array['result'][i]['recognition_words'][0])
        str = ' '.join(print)
        return render_template('ocr/ocr_test.html', real=str)