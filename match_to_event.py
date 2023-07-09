from datetime import timedelta
from idutils import IDUtils
from match import MatchInfo

class MatchToEvent:
    def __get_id(self, match: MatchInfo):
        return IDUtils.generateID(match.isHome, match.opponent, match.competition)

    def __get_summary(self, match: MatchInfo):
        return self.__get_teams(match)

    def __get_teams(self, match: MatchInfo):
        home = match.team if match.isHome else match.opponent
        away = match.opponent if match.isHome else match.team
        return f'{home} x {away}'

    def __get_description(self, match: MatchInfo):
        return f'{self.__get_teams(match)}\n{match.competition}'

    def __get_datetime(self, datetime):
        return {
            'dateTime': datetime.isoformat(),
            'timeZone': 'America/Sao_Paulo'
        }

    def __get_location(self, match):
        return ''

    def convert(self, match: MatchInfo):
        event_id = self.__get_id(match)
        summary = self.__get_summary(match)
        location = self.__get_location(match)
        description = self.__get_description(match)
        start = self.__get_datetime(match.datetime)
        end = self.__get_datetime(match.datetime + timedelta(hours=2))

        return {
            'id': event_id,
            'summary': summary,
            'location': location,
            'description': description,
            'start': start,
            'end': end,
            'colorId': 10
        }

    