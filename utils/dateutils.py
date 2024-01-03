import re
from datetime import datetime
from constants import SERVER_TIME_ZONE, LOCAL_TIME_ZONE
from zoneinfo import ZoneInfo

class DateUtils:
    @staticmethod
    def is_valid_time(time: str):
        time_pattern = r"\d{2}\s:\s\d{2}"
        return re.match(time_pattern, time)

    @staticmethod
    def get_local_datetime(date: str, time: str) -> datetime:
        local_tz = ZoneInfo(LOCAL_TIME_ZONE)
        server_tz = ZoneInfo(SERVER_TIME_ZONE)
        pattern = '%d/%m/%y %H : %M'
        server_dt = datetime.strptime(date+" "+time, pattern).replace(tzinfo=server_tz)
        return server_dt.astimezone(local_tz)