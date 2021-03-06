from flask import Blueprint, url_for, flash
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')


# 메인페이지 HTML 렌더링 (로그인 페이지)
@bp.route('/')
def home_page():
    return redirect(url_for('login.main'))

