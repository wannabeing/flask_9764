from flask import Blueprint, render_template, request, url_for, g, flash

from models import Board, board_voter, Comment
from forms import BoardForm
from datetime import datetime
from werkzeug.utils import redirect
from blog import db
from views.login_views import login_required
from sqlalchemy import func

bp = Blueprint('cal', __name__, url_prefix='/cal')


# 캘린더 메인 페이지 렌더링
@bp.route('/')
def main():
    return render_template('calendar/cal_main.html')


@bp.route('/test/')
def test():
    return render_template('test.html')