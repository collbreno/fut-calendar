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
    
    @staticmethod
    def get_datetime_from_espn_api(str_date: str) -> datetime:
        return datetime.strptime(str_date, "%Y-%m-%dT%H:%M%z").astimezone(ZoneInfo(LOCAL_TIME_ZONE))
    
    @staticmethod
    def now() -> datetime:
        return datetime.now(ZoneInfo(LOCAL_TIME_ZONE))
    
    @staticmethod
    def get_datetime_from_timestamp(ts: str) -> datetime:
        # MAY NOT WORK WHEN RUNNING IN GOOGLE CLOUD
        local_tz = ZoneInfo(LOCAL_TIME_ZONE)
        return datetime.fromtimestamp(int(ts)).replace(tzinfo=local_tz)