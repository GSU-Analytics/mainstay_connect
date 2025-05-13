
from datetime import datetime, timedelta

def generate_dt_days_range(start_date: datetime, end_date: datetime):
    '''Create a list of Python `datetime` objects, one for each day between
    `start_date` and `end_date`.
    '''
    current_date = start_date
    date_ranges = [start_date]
    while current_date < end_date:
        current_date += timedelta(days=1)
        date_ranges.append(current_date)
    return date_ranges