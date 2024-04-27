from bs4 import BeautifulSoup
import requests

from constants import USER_AGENT
from models.competition import Competition

class CompetitionScraper:
    def __init__(self) -> None:
        self.headers = {
            "user-agent": USER_AGENT
        }

    def __get_id(self, soup: BeautifulSoup):
        li = soup.find('div', id='subheading').find('ul').find('li')
        link = li.find('a')['href']
        parts = link.split('/')
        return f'{parts[2]}_{parts[3]}'
        

    def __get_teams(self, soup: BeautifulSoup):
        teams = []
        tables = soup.select('table.leaguetable.detailed-table')
        for table in tables:
            print('table found')
            tbody = table.find('tbody')
            rows = tbody.find_all('tr')
            for row in rows:
                team_url = row.find('td', class_='team').find('a')['href']
                teams.append(team_url.split('/')[-2])

        return teams
    
    def __get_name(self, soup: BeautifulSoup):
        h1_tag = soup.find('div', id='subheading').find('h1')
        return h1_tag.get_text()

    def get(self, competition_url):
        response = requests.get(competition_url, headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")
        return Competition(
            id=self.__get_id(soup),
            name=self.__get_name(soup),
            teams=self.__get_teams(soup)
        )

