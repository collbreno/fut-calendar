import requests
from models.espn_competition import EspnCompetition
from utils.dict_utils import DictUtils

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
    
    def get_map_name(self, league_slug, lang):
        mapper = {}
        url = f'https://site.api.espn.com/apis/site/v2/sports/soccer/{league_slug}/teams'
        response = requests.get(url, params={'lang': lang}).json()
        league = response['sports'][0]['leagues'][0]
        for league_team in league['teams']:
            team = league_team['team']
            mapper[team['id']] = team['name']
        return DictUtils.sort_as_int(mapper)