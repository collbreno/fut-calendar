from bs4 import BeautifulSoup
import requests
from constants import USER_AGENT
from dateutils import DateUtils
from match import MatchInfo

class MatchesScraper:
    def __init__(self, team, url) -> None:
        self.team = team
        self.url = url
        self.headers = {
            "user-agent": USER_AGENT
        }

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
            if (DateUtils.is_valid_time(time)):
                if home != self.team and away != self.team:
                    raise Exception(f"Favorite team ({self.team}) isn't {home} nor {away}")
                return MatchInfo(
                    team = self.team,
                    datetime = DateUtils.get_local_datetime(date, time),
                    competition = competition,
                    isHome = self.team==home,
                    opponent = away if self.team == home else home,
                )

    def get_scheduled_matches(self):
        response = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="matches")
        tbody = table.find("tbody")
        rows = tbody.find_all("tr")

        for row in rows:
            match = self.__get_match_info(row)
            if match is not None:
                yield match


