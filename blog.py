from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flaskext.markdown import Markdown
from flask_simplemde import SimpleMDE

import config

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # file upload 용량 제한 (16MB)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    # markdown
    app.config["SIMPLEMDE_JS_IIFE"] = True
    app.config["SIMPLEMDE_USE_CDN"] = True

    SimpleMDE(app)
    Markdown(app, extensions=['nl2br', 'fenced_code'])

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    #   from models import Question, Answer

    # 블루프린트
    from views import main_views, file_views, login_views, \
        question_views, answer_views, vote_views, board_views, comment_views, \
        ocr_views, calendar_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(file_views.bp)
    app.register_blueprint(login_views.bp)

    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(board_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(calendar_views.bp)
    app.register_blueprint(vote_views.bp)
    app.register_blueprint(ocr_views.bp)

    # 날짜, 콤마 필터
    from filter import format_datetime, detail_datetime, simple_number
    # 'datetime' 이름으로 필터 등록
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['detail_datetime'] = detail_datetime
    app.jinja_env.filters['simple_number'] = simple_number

    # 에러 404 HTML 렌더링
    @app.errorhandler(404)
    def page_not_found(error):
         app.logger.error(error)  # 어떠한 오류나 특정 요청에 대한 로그를 남기고자 로깅을 한다. cmd 창에서 확인 가능
         return render_template('404.html'), 404    # 존재하지 않는 페이지를 입력하면 404.html을 불러온다.
    return app
