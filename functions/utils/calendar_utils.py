import re

class CalendarUtils:
    @staticmethod
    def format_id(id: str):
        pattern = r'[^a-v0-9]'
        return re.sub(pattern, '', id)