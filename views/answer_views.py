from datetime import datetime

from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect

from blog import db
from models import Question, Answer
from forms import AnswerForm

bp = Blueprint('answer', __name__, url_prefix='/answer')


@bp.route('create/<int:question_id>/form')
def form(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('answer/answer_form.html', question=question)


@bp.route('create/<int:question_id>/check', methods=('POST',))
def check(question_id):
    question = Question.query.get_or_404(question_id)
    content = request.form['content']
    answer = Answer(content=content, create_date=datetime.now())
    question.answer_set.append(answer)
    db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))