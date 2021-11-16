# datetime 객체를 보기 편한 문자열로 만드는 필터.py

from datetime import datetime, timedelta

import locale
locale.setlocale(locale.LC_ALL, '')


def format_datetime(value, fmt='%m월 %d일'):
    now = datetime.now()
    time = now - value

    if time < timedelta(minutes=1):
        return '방금 전'
    elif time < timedelta(hours=1):
        return str(int(time.seconds / 60)) + '분 전'
    elif time < timedelta(days=1):
        return str(int(time.seconds / 3600)) + '시간 전'
    elif time < timedelta(days=7):
        time = datetime.now().date() - value.date()
        return str(time.days) + '일 전'
    else:
        return value.strftime(fmt)


# question_detail 에 사용할 필터
def detail_datetime(value, fmt='%Y.%m.%d %H:%M'):
    return value.strftime(fmt)


# 숫자 ,(콤마) 붙이는 필터
def simple_number(value):
    return '{:,}'.format(value)