import datetime
def get_month_key(date: datetime) -> str:
    return date.strftime("%Y-%m")