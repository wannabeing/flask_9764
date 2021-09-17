from blog import db
from forms import UserCreateForm
from models import User
from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect


bp = Blueprint("login", __name__, url_prefix='/login')


# 로그인 메인 HTML 렌더링
@bp.route('/main/')
def login_page():
    return render_template('login/login_login.html')


# 회원가입 HTML 렌더링
@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login.login_page'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('login/login_sign.html', form=form)