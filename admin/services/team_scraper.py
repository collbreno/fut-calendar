from bs4 import BeautifulSoup
import requests

from constants import USER_AGENT

class TeamScraper:
    def __init__(self) -> None:
        self.headers = {
            "user-agent": USER_AGENT
        }

    def __get_url(self, team_id):
        return f'https://br.soccerway.com/teams/x/x/{team_id}/'

    def __get_by_dropdown(self, soup: BeautifulSoup):
        select = soup.find('select', {'name': 'team_id'})
        selected = select.find('option', selected=True)
        return selected.text
    
    def __get_by_subheading(self, soup: BeautifulSoup):
        h1_tag = soup.find('div', id='subheading').find('h1')
        return h1_tag.get_text()

    def get_name(self, team_id):
        response = requests.get(self.__get_url(team_id), headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")
        try:
            return self.__get_by_dropdown(soup)
        except:
            return self.__get_by_subheading(soup)


