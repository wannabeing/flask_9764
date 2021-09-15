from flask import Blueprint, url_for
from werkzeug.utils import redirect
from blog import *

bp = Blueprint('main', __name__, url_prefix='/')


# 메인페이지 HTML 렌더링 (로그인 페이지)
@bp.route('/')
def home_page():
    return redirect(url_for('login.login_page'))

