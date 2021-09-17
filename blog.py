from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from models import Question, Answer

    # 블루프린트
    from views import main_views, file_views, login_views, question_views, answer_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(file_views.bp)
    app.register_blueprint(login_views.bp)

    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)

    # 날짜 필터
    from filter import format_datetime
    # 'datetime' 이름으로 필터 등록
    app.jinja_env.filters['datetime'] = format_datetime

    # 에러 404 HTML 렌더링
    @app.errorhandler(404)
    def page_not_found(error):
         app.logger.error(error)  # 어떠한 오류나 특정 요청에 대한 로그를 남기고자 로깅을 한다. cmd 창에서 확인 가능
         return render_template('404.html'), 404 # 존재하지 않는 페이지를 입력하면 404.html을 불러온다.

    return app
