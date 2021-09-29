from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from blog import db
from forms import UserCreateForm, UserLoginForm
from models import User

import functools

bp = Blueprint("login", __name__, url_prefix='/login')


# 모든 라우트함수보다 먼저 실행되면서 로그인한 사용자 정보를 조회하는 함수
@bp.before_app_request
def logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


# 로그인 메인 HTML 렌더링
@bp.route('/main/')
def main():
    return render_template('login/login_main.html')


# 회원가입 HTML 렌더링, POST = 계정등록, GET = 회원가입 템플릿 렌더링
@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        name=form.name.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login.main'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('login/login_sign.html', form=form)


# 로그인 HTML 렌더링, POST = 로그인, GET = 로그인 템플릿 렌더링
@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('login.main'))
        flash(error)
    return render_template('login/login_login.html', form=form)


# 로그아웃 후, 메인페이지 렌더링
@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login.main'))


# 로그아웃 상태에서 게시판 이용할 때, 로그인페이지로 리다이렉트
# 다른 함수에 @login_required 애너테이션을 지정하면, 아래 함수가 먼저 실행된다.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login.login'))
        return view(**kwargs)
    return wrapped_view