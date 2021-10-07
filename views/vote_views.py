from flask import Blueprint, url_for, flash, g
from werkzeug.utils import redirect

from blog import db
from models import Question, Answer, Board
from views.login_views import login_required

bp = Blueprint('vote', __name__, url_prefix='/vote')


@bp.route('/question/<int:question_id>/')
@login_required
def question(question_id):
    _question = Question.query.get_or_404(question_id)
    if g.user == _question.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    elif g.user in _question.voter:
        flash('이미 추천했습니다.')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))


@bp.route('/vote/<int:answer_id>/')
@login_required
def answer(answer_id):
    _answer = Answer.query.get_or_404(answer_id)
    if g.user == _answer.user:
        flash('본인이 작성한 글은 추천할 수 없습니다')
    elif g.user in _answer.voter:
        flash('이미 추천했습니다.')
    else:
        _answer.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=_answer.question.id))


@bp.route('/board/<int:question_id>/')
@login_required
def board(board_id):
    _board = Board.query.get_or_404(board_id)
    if g.user == _board.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    elif g.user in _board.voter:
        flash('이미 추천했습니다.')
    else:
        _board.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('board.detail', board_id=board_id))