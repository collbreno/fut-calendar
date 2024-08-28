
from google.cloud.firestore import Client
from services.calendar_api import CalendarOAuthApi
from services.espn_competition_scraper import EspnCompetitionScraper
import json
from models.espn_team import EspnTeam

class CalendarCreator:
    def __init__(self, db: Client, calendar_api: CalendarOAuthApi) -> None:
        self.db = db
        self.calendar_api = calendar_api
        self.scraper = EspnCompetitionScraper()

    def __get_calendar_name(self, team: EspnTeam):
        name = f'Jogos {team.name}'        
        if team.flag is not None and len(team.flag) > 0:
            name += f' {team.flag}'
        return name

    def create_calendar(self, team: EspnTeam):
        calendar_id = self.calendar_api.create_calendar(self.__get_calendar_name(team))
        self.calendar_api.make_public(calendar_id)
        self.calendar_api.add_as_writer(calendar_id, '156268949150-compute@developer.gserviceaccount.com')
        return calendar_id