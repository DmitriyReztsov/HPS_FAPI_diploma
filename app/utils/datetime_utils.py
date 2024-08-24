from datetime import date, datetime, timedelta
from app.db.models.report import ReportPeriodChoices


def daterange(start_date: date, end_date: date):
    days = int((end_date - start_date).days)
    for n in range(days):
        yield start_date + timedelta(n)


def get_period_from_datetime(init_datetime: datetime, period: str) -> str:
    match period.lower():
        case ReportPeriodChoices.DAILY.value:
            return tuple(int(date_frag) for date_frag in str(init_datetime.date()).split("-"))
        case ReportPeriodChoices.MONTHLY.value:
            return (init_datetime.year, init_datetime.month)
        case ReportPeriodChoices.QUARTERLY.value:
            return (init_datetime.year, (init_datetime.month - 1) // 3 + 1)
        case ReportPeriodChoices.ANNUALLY.value:
            return (init_datetime.year,)


def get_str_key(key_elems: list, period: str) -> str:
    match period.lower():
        case ReportPeriodChoices.DAILY.value:
            return str(datetime.strptime("-".join(key_elems), "%Y-%m-%d").date())
        case ReportPeriodChoices.MONTHLY.value:
            return str(datetime.strptime("-".join(key_elems), "%Y-%m").date())[:-3]
        case ReportPeriodChoices.QUARTERLY.value:
            return f"{key_elems[0]}-Q{key_elems[1]}"
        case ReportPeriodChoices.ANNUALLY.value:
            return str(key_elems[0])
