from datetime import datetime


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


def validate_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False