from datetime import date, datetime


def date_today():
    """Returns date in YYYY-MM-DD"""
    return date.today().strftime("%Y-%m-%d")


def time_now():
    """Returns time in H:M:S"""
    return datetime.now().strftime("%H:%M:%S")


def week_day_name(date_YYYY_MM_DD: str):
    """Be sure to supply date in YYYY-MM-DD. Returns a day name of the week."""
    return datetime.strptime(date_YYYY_MM_DD, "%Y-%m-%d").strftime("%A")


def day_name_today():
    """Returns today's day name"""
    return week_day_name(date_today())


if __name__ == "__main__":
    print(time_now())
