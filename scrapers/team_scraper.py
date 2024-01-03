from bs4 import BeautifulSoup
import requests

from constants import USER_AGENT

class TeamScraper:
    def __init__(self) -> None:
        self.headers = {
            "user-agent": USER_AGENT
        }

    def __get_img_url(self, soup):
        logo_element = soup.find('div', class_='logo')
        img_element = logo_element.find('img')
        return img_element.get('src')

    def __get_matches_url(self, team_url):
        return team_url.strip()+'/matches/'

    def __get_team_name(self, soup):
        subheading_element = soup.find('div', id='subheading')
        h1_element = subheading_element.find('h1')
        return h1_element.get_text()

    def get_info(self, team_url):
        response = requests.get(team_url, headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")
        img = self.__get_img_url(soup)
        matches = self.__get_matches_url(team_url)
        team_name = self.__get_team_name(soup)

        return {
            'team': team_name,
            'matches_url': matches,
            'img_url': img
        }