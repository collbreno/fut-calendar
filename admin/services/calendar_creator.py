
from google.cloud.firestore import Client
from services.calendar_api import CalendarOAuthApi
from services.espn_competition_scraper import EspnCompetitionScraper
import json
from models.espn_team import EspnTeam

class CalendarCreator:
    def __init__(self, calendar_api: CalendarOAuthApi) -> None:
        self.calendar_api = calendar_api
        self.scraper = EspnCompetitionScraper()

    def __get_calendar_name(self, name: str, flag: str) -> str:
        name = f'Jogos {name}'        
        if flag is not None and len(flag) > 0:
            name += f' {flag}'
        return name

    def create_calendar(self, name: str, flag: str) -> str:
        calendar_id = self.calendar_api.create_calendar(self.__get_calendar_name(name, flag))
        self.calendar_api.make_public(calendar_id)
        self.calendar_api.add_as_writer(calendar_id, '156268949150-compute@developer.gserviceaccount.com')
        return calendar_id