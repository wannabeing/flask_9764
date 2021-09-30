from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from blog import db
from models import Question, Answer
from forms import AnswerForm
from views.login_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')


@bp.route('/create/<int:question_id>/form', methods=('POST', 'GET'))
@login_required
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    # if 문은 POST 방식으로 들어온 데이터를 저장하는 코드
    if request.method == 'POST' and form.validate_on_submit():
        # form 에서 content 내용을 변수 content 에 저장
        content = request.form['content']
        # g.user 는 login_views.py의 로그인한 사용자 정보이다.
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        question.answer_set.append(answer)
        db.session.add(answer)
        db.session.commit()
        # 답변 제출 시, 답변에 대한 질문 글 출력하기 위한 함수 호출
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('answer/answer_form.html', form=form, question=question)


@bp.route('/modify/<int:answer_id>/form', methods=('POST', 'GET'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=answer.question.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=answer.question.id))
    else:   # GET 요청
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_modify_form.html', form=form)    # 수정하기 버튼 클릭시, 렌더링


@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))