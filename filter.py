# datetime 객체를 보기 편한 문자열로 만드는 필터파일

import locale
locale.setlocale(locale.LC_ALL, '')

def format_datetime(value, fmt=''):
    return value.strftime(fmt)