from flask import Blueprint, url_for, render_template, flash, request, session, g, jsonify
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
    if request.method == 'POST':
        if request.get_json():  # 비동기통신일 때 (유효성검사)
            result = request.get_json()

            if result['kind'] == 'id':  # 아이디 중복 확인일 때
                id = result['data']
                if User.query.filter_by(username=id).first() is None:
                    return jsonify(result="success", kind="id")  # 성공시
                else:
                    return jsonify(result="error", kind="id")  # 실패시

            elif result['kind'] == 'email':  # 이메일 중복 확인일 때
                email = result['data']
                if User.query.filter_by(email=email).first() is None:
                    return jsonify(result="success", kind="email")   # 성공시
                else:
                    return jsonify(result="error", kind="email")   # 실패시

            elif result['kind'] == 'submit':    # 회원가입 폼 전송
                user = User(username=result['id'],
                            password=generate_password_hash(result['pw']),
                            name=result['name'], email=result['email'],
                            fir_joo=result['fir_joo'], sec_joo=result['sec_joo'],
                            tel=result['tel'])
                db.session.add(user)
                db.session.commit()
                return jsonify()
            else:
                pass
    return render_template('login/login_sign.html')


# 로그인 HTML 렌더링, POST = 로그인, GET = 로그인 템플릿 렌더링
@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    url = request.args.get('url')
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
            # 이전 페이지(GET)가 None 이면 login.main redirect
            # else 이면 이전 페이지로 redirect
            if url is None:
                return redirect(url_for('login.main'))
            else:
                return redirect(url)
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
            return redirect(url_for('login.login', url=request.url))
        return view(**kwargs)
    return wrapped_view