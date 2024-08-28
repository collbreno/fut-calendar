import requests
from models.espn_team import EspnTeam

class EspnTeamScraper:
    def __init__(self) -> None:
        self.params = {
            'lang': 'pt',
            'region': 'br'
        }

    def get(self, team_id: str, flag=None) -> EspnTeam:
        url = f'https://site.api.espn.com/apis/site/v2/sports/soccer/all/teams/{team_id}'
        response = requests.get(url, params=self.params).json()
        team = response['team']
        return EspnTeam(
            image_url=team['logos'][0]['href'],
            slug=team['slug'],
            name=team['name'],
            id=team['id'],
            flag=flag,
        )