import os

# 현재 코드를 담고 있는 파일의 위치
BASE_DIR = os.path.dirname(__file__)

# DB 접속 주소
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'blog.db'))
# SQLAlchemy 이벤트 처리 옵션, 필요하지 않으므로 비활성화(False)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"