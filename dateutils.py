import re
from datetime import datetime, timedelta

class DateUtils:
    @staticmethod
    def is_valid_time(time: str):
        time_pattern = r"\d{2}\s:\s\d{2}"
        return re.match(time_pattern, time)

    @staticmethod
    def get_local_datetime(date: str, time: str):
        return datetime.strptime(date+" "+time, "%d/%m/%y %H : %M") - timedelta(hours=5)