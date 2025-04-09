import datetime as da
from datetime import datetime as dada
from record import Record, Birthday


def get_congratilation_date(birthday: Birthday, year: int) -> dada.date:
    congratilation_date = da.date(year, birthday.value.month, birthday.value.day)
    if congratilation_date.isoweekday() == 6:
        congratilation_date = congratilation_date + da.timedelta(days=2)
    elif congratilation_date.isoweekday() == 7:
        congratilation_date = congratilation_date + da.timedelta(days=1)
    return congratilation_date


def get_upcoming_birthdays(records: list[Record], days: int = 7) -> list[Record]:
    result = []
    today = dada.today().date()
    for record in records:
        if record.birthday:
            congratulation_date = get_congratilation_date(record.birthday, today.year)
            delta = (congratulation_date - today).days
            if delta < 0:
                congratulation_date = get_congratilation_date(
                    record.birthday, today.year + 1
                )
                delta = (congratulation_date - today).days
            if 0 <= delta < days:
                result.append(record)
    return result
