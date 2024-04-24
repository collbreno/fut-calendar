from datetime import timedelta
from constants import LOCAL_TIME_ZONE, MATCH_DURATION
from models.match import Match
from utils.calendar_utils import CalendarUtils
import re

class MatchConverter:
    def __get_id(self, match: Match):
        return CalendarUtils.format_id(match.id)

    def __get_summary(self, match: Match):
        teams = f'{match.home} x {match.away}'
        if match.flag is not None and match.flag != '':
            teams += f' ({match.flag})'
        return teams

    def __get_description(self, match: Match):
        return match.competition

    def __get_datetime(self, datetime):
        return {
            'dateTime': datetime.isoformat(),
            'timeZone': LOCAL_TIME_ZONE
        }

    def __get_location(self, match):
        return ''

    def convert(self, match: Match):
        event_id = self.__get_id(match)
        summary = self.__get_summary(match)
        location = self.__get_location(match)
        description = self.__get_description(match)
        start = self.__get_datetime(match.datetime)
        end = self.__get_datetime(match.datetime + timedelta(hours=MATCH_DURATION))

        return {
            'id': event_id,
            'summary': summary,
            'location': location,
            'description': description,
            'start': start,
            'end': end,
            'colorId': 10
        }

    