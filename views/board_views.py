from flask import Blueprint, render_template, request, url_for, g, flash

from models import Board, board_voter, Comment
from forms import BoardForm
from datetime import datetime
from werkzeug.utils import redirect
from blog import db
from views.login_views import login_required
from sqlalchemy import func

bp = Blueprint('board', __name__, url_prefix='/board')


@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지번호가 없으면 default 로 페이지1을 출력한다.
    kw = request.args.get('kw', type=str, default='')  # 검색어
    so = request.args.get('so', type=str, default='recent')  # 정렬, default 는 최신순('recent')

    # 정렬
    if so == 'recommend':  # 추천 수가 많은 게시물
        sub_query = db.session.query(board_voter.c.board_id, func.count('*').label('num_voter')) \
            .group_by(board_voter.c.board_id).subquery()
        board_list = Board.query \
            .outerjoin(sub_query, Board.id == sub_query.c.board_id) \
            .order_by(sub_query.c.num_voter.desc(), Board.create_date.desc())
    elif so == 'popular':  # 답변 수가 많은 게시물
        sub_query = db.session.query(Comment.board_id, func.count('*').label('num_board')) \
            .group_by(Comment.board_id).subquery()
        board_list = Board.query \
            .outerjoin(sub_query, Board.id == sub_query.c.board_id) \
            .order_by(sub_query.c.num_board.desc(), Board.create_date.desc())
    elif so == 'hit':  # 조회 수가 많은 게시물
        board_list = Board.query.order_by(Board.hits.desc())
    else:  # recent, 기존 게시물
        board_list = Board.query.order_by(Board.create_date.desc())
    # 페이징
    board_list = board_list.paginate(page, per_page=5)
    return render_template('board/board_list.html', board_list=board_list, page=page, so=so)


@bp.route('/detail/<int:board_id>/')
def detail(board_id):
    form = BoardForm()
    board = Board.query.get_or_404(board_id)
    # 조회수 증가를 위한 코딩, but 새로고침시에도 조회수가 올라가므로 새로운 방법을 넣어야 함.
    board.hits += 1
    db.session.add(board)
    db.session.commit()
    return render_template('board/board_detail.html', board=board, form=form)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = BoardForm()
    if request.method == 'POST' and form.validate_on_submit():
        board = Board(subject=form.subject.data, content=form.content.data,
                      create_date=datetime.now(), user=g.user)
        db.session.add(board)
        db.session.commit()
        return redirect(url_for('board.detail', board_id=board.id))
    return render_template('board/board_form.html', form=form)


# GET = 수정 버튼 클릭
@bp.route('/modify/<int:board_id>', methods=('GET', 'POST'))
@login_required
def modify(board_id):
    board = Board.query.get_or_404(board_id)
    if g.user != board.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('board.detail', board_id=board_id))
    if request.method == 'POST':  # POST 요청
        form = BoardForm()
        if form.validate_on_submit():
            form.populate_obj(board)
            board.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('board.detail', board_id=board_id))
    else:  # GET 요청
        form = BoardForm(obj=board)
    return render_template('board/board_form.html', form=form)


# 삭제 버튼 클릭
@bp.route('/delete/<int:board_id>')
@login_required
def delete(board_id):
    board = Board.query.get_or_404(board_id)
    if g.user != board.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('board.detail', board_id=board_id))
    db.session.delete(board)
    db.session.commit()
    return redirect(url_for('board._list'))
