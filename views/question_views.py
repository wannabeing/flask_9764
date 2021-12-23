from flask import Blueprint, render_template, request, url_for, g, flash

from models import Question, Answer, User, question_voter
from forms import QuestionForm, AnswerForm
from datetime import datetime
from werkzeug.utils import redirect
from blog import db
from views.login_views import login_required
from sqlalchemy import func

bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/list/')
def _list():
    # 입력 파라미터
    page = request.args.get('page', type=int, default=1)  # 페이지번호가 없으면 default 로 페이지1을 출력한다.
    kw = request.args.get('kw', type=str, default='')   # 검색어
    so = request.args.get('so', type=str, default='recent')  # 정렬, default 는 최신순('recent')

    # 정렬
    if so == 'recommend':   # 추천 수가 많은 게시물
        sub_query = db.session.query(question_voter.c.question_id, func.count('*').label('num_voter')) \
            .group_by(question_voter.c.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_voter.desc(), Question.create_date.desc())
    elif so == 'popular':   # 답변 수가 많은 게시물
        sub_query = db.session.query(Answer.question_id, func.count('*').label('num_answer')) \
            .group_by(Answer.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_answer.desc(), Question.create_date.desc())
    elif so == 'hit':   # 조회 수가 많은 게시물
        question_list = Question.query.order_by(Question.hits.desc())
    else:  # recent, 기존 게시물
        question_list = Question.query.order_by(Question.create_date.desc())
    # 페이징
    question_list = question_list.paginate(page, per_page=5)
    return render_template('question/question_list.html', question_list=question_list, page=page, so=so)


@bp.route('/detail/<int:question_id>/')
@login_required
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    # 조회수 증가를 위한 코딩, but 새로고침시에도 조회수가 올라가므로 새로운 방법을 넣어야 함.
    question.hits += 1
    db.session.add(question)
    db.session.commit()
    return render_template('question/question_detail.html', question=question, form=form)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data,
                            create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('question._list'))
        # return redirect(url_for('question.detail', question_id=question.id)), 모자른 조회수 기능 때문에
    return render_template('question/question_form.html', form=form)


# GET = 수정 버튼 클릭
@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':  # POST 요청
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET 요청
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)


# 삭제 버튼 클릭
@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))