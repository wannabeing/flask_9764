from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목을 입력하세용.')])
    content = TextAreaField('내용', validators=[DataRequired('내용을 입력하세용.')])


class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용을 입력하세용.')])


class UserCreateForm(FlaskForm):
    username = StringField('이름', validators=[DataRequired('이름을 입력하세용'), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니당')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired('이메일을 입력하세용'), Email()])