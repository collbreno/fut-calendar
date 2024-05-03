from bs4 import BeautifulSoup
import requests

from constants import USER_AGENT
from utils.date_utils import DateUtils
from models.match import Match

class MatchesScraper:
    def __init__(self, soccerway_id, flag) -> None:
        self.url = f'https://br.soccerway.com/teams/x/x/{soccerway_id}/matches/'
        self.flag = flag
        headers = {
            "user-agent": USER_AGENT
        }
        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="matches")
        tbody = table.find("tbody")
        self.rows = tbody.find_all("tr")

    def __get_td_text(self, row, column_name: str) -> str:
        return row.find("td", class_=column_name).get_text().strip()

    def __get_td_title(self, row, column_name: str) -> str:
        return row.find("td", class_=column_name).find("a").get("title")

    def __get_match_info(self, row):
            date = self.__get_td_text(row, "full-date")
            time = self.__get_td_text(row, "score-time")
            competition = self.__get_td_title(row, "competition")
            home = self.__get_td_text(row, "team-a")
            away = self.__get_td_text(row, "team-b")
            id = row.get('data-event-id')
            if (DateUtils.is_valid_time(time)):
                return Match(
                    id=id,
                    home = home,
                    away = away,
                    datetime = DateUtils.get_local_datetime(date, time),
                    competition = competition,
                    flag = self.flag,
                )

    def get_scheduled_matches(self):
        for row in self.rows:
            match = self.__get_match_info(row)
            if match is not None:
                yield match

    def get_cancelled_match_ids(self):
        for row in self.rows:
            time = self.__get_td_text(row, 'score-time')
            if time == 'ADIA' or time == 'CANC':
                yield row.get('data-event-id')

