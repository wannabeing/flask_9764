from blog import *
from flask import Blueprint


bp = Blueprint("login", __name__, url_prefix='/login')


# 로그인 메인 HTML 렌더링
@bp.route('/main/')
def login_page():
    return render_template('login.html')


# 회원가입 HTML 렌더링
@bp.route('/register/')
def register_page():
    return render_template('register.html')