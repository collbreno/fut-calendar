import requests
from models.match import Match
from utils.date_utils import DateUtils
from services.teams_mapper import TeamsMapper

class EspnTeamScraper:
    def __init__(self, team_id: str, flag: str, mapper: TeamsMapper) -> None:
        self.team_id = team_id
        self.mapper = mapper
        self.flag = flag

    def get_scheduled_matches(self):
        url = f'https://site.web.api.espn.com/apis/site/v2/sports/soccer/all/teams/{self.team_id}/schedule'
        params = {
            'fixture': 'true',
            'lang': 'pt',
            'region': 'br',
        }
        response = requests.get(url, params=params)
        events = response.json()['events']
        for event in events:
            if (event['timeValid']):
                competition = event['competitions'][0]
                home = competition['competitors'][0]['team']
                away = competition['competitors'][1]['team']
                competition_name = event['league']['name']
                yield Match(
                    id=event['id'],
                    flag=self.flag,
                    home=self.__get_team_name(home),
                    away=self.__get_team_name(away),
                    competition=self.__get_description(home, away, competition_name),
                    datetime=DateUtils.get_datetime_from_espn_api(event['date']),
                )

    def __get_team_name(self, team: dict) -> str:
        default = team.get('abbreviation', team['displayName'])
        if self.mapper is None:
            return default
        else:
            return self.mapper.get_team(team['id'], default)
        
    def __get_description(self, home: dict, away: dict, competition: str) -> str:
        if self.mapper is None:
            return f'{home['displayName']} x {away['displayName']}\n{competition}'
        else:
            return self.mapper.get_description(
                home_id=home['id'], 
                away_id=away['id'], 
                competition=competition,
            )