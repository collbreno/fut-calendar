import requests
from models.espn_competition import EspnCompetition

class EspnCompetitionScraper:
    def __init__(self) -> None:
        self.params = {
            'lang': 'pt',
            'region': 'br'
        }

    def get(self, league_slug) -> EspnCompetition:
        url = f'https://site.api.espn.com/apis/site/v2/sports/soccer/{league_slug}/scoreboard'
        response = requests.get(url, params=self.params).json()
        league = response['leagues'][0]
        return EspnCompetition(
            logo=league['logos'][0]['href'],
            slug=league['slug'],
            name=league['name']
        )