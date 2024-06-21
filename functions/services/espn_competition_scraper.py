import requests
from models.match import Match
from utils.date_utils import DateUtils
from services.teams_mapper import TeamsMapper

class EspnCompetitionScraper:
    def __init__(self, league_slug: str, flag: str, mapper: TeamsMapper) -> None:
        self.slug = league_slug
        self.flag = flag
        self.mapper = mapper
        url = f'https://site.api.espn.com/apis/site/v2/sports/soccer/{self.slug}/scoreboard'
        params = {
            'dates': self.__get_date_range(),
            'lang': 'pt',
            'region': 'br'
        }
        self.response = requests.get(url, params=params).json()

    def get_scheduled_matches(self):
        events = self.response['events']
        for event in events:
            competition = event['competitions'][0]
            if (competition['timeValid']):
                home = competition['competitors'][0]['team']
                away = competition['competitors'][1]['team']
                competition_name = self.response['leagues'][0]['name']
                yield Match(
                    id=event['id'],
                    flag=self.flag,
                    datetime=DateUtils.get_datetime_from_espn_api(event['date']),
                    home=self.__get_team_name(home),
                    away=self.__get_team_name(away),
                    competition=self.__get_description(home, away, competition_name),
                )
    
    def __get_team_name(self, team: dict) -> str:
        default = team.get('abbreviation', team['displayName'])
        if self.mapper is None:
            return default
        else:
            return self.mapper.get_team(team['id'], default)
        
    def __get_description(self, home: dict, away: dict, competition: str) -> str:
        if self.mapper is None:
            return competition
        else:
            return self.mapper.get_description(
                home_id=home['id'], 
                away_id=away['id'], 
                competition=competition,
            )
    
    def __get_date_range(self):
        url = f'https://sports.core.api.espn.com/v2/sports/soccer/leagues/{self.slug}/calendar/ondays'
        response = requests.get(url)
        json = response.json()
        start_date = json['eventDate']['dates'][0]
        end_date = json['eventDate']['dates'][-1]
        return f'{self.__format_date(start_date)}-{self.__format_date(end_date)}'
    
    def __format_date(self, str_date):
        return DateUtils.get_datetime_from_espn_api(str_date).strftime('%Y%m%d')