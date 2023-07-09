from bs4 import BeautifulSoup
import requests
from dateutils import DateUtils
from match import MatchInfo

class Scraper:
    def __init__(self) -> None:
        self.team = "Fluminense"
        self.url = "https://br.soccerway.com/teams/brazil/fluminense-football-club/312/matches/"
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

    def __get_column_text(self, row, column_name: str) -> str:
        return row.find("td", class_=column_name).get_text().strip()

    def __get_match_info(self, row):
            date = self.__get_column_text(row, "full-date")
            time = self.__get_column_text(row, "score-time")
            competition = self.__get_column_text(row, "competition")
            home = self.__get_column_text(row, "team-a")
            away = self.__get_column_text(row, "team-b")
            if (DateUtils.is_valid_time(time)):
                if home != self.team and away != self.team:
                    raise Exception(f"Favorite team ({self.team}) isn't {home} nor {away}")
                return MatchInfo(
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


