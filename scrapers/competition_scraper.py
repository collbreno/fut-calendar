from bs4 import BeautifulSoup
import requests

from constants import BASE_URL, USER_AGENT

class CompetitionScraper:
    def __init__(self) -> None:
        self.headers = {
            "user-agent": USER_AGENT
        }

    def get_teams(self, competition_url):
        response = requests.get(competition_url, headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")

        table = soup.find('table', class_='leaguetable')
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')

        for row in rows:
            td_team = row.find('td', class_='large-link')
            a_element = td_team.find('a')
            team_url = BASE_URL+a_element.get('href')
            yield team_url
        