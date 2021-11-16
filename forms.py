from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목을 입력하세용.')])
    content = TextAreaField('내용', validators=[DataRequired('내용을 입력하세용.')])


class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용을 입력하세용.')])


class UserCreateForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired('아이디를 정확히 입력하세요 (최소3글자 이상)'), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired('입력하세용.'), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired('비밀번호가 일치하지 않습니다')])
    name = StringField('이름', validators=[DataRequired(), Length(min=2, max=10)])
    email = EmailField('이메일', validators=[DataRequired('입력하세용.'), Email('이메일 형식이 아닙니다.')])


class UserLoginForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired('아이디를 정확히 입력하세용.'), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired('비밀번호를 정확히 입력하세용.')])


class BoardForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목을 입력하세용')])
    content = TextAreaField('내용', validators=[DataRequired('내용을 입력하세용')])


class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용을 입력하세용')])