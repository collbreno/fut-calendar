from google.cloud.firestore import Client
from services.calendar_api import CalendarOAuthApi
from services.calendar_creator import CalendarCreator
from models.espn_team import EspnTeam

class EspnTeamCreator:
    def __init__(self, db: Client, calendar_api: CalendarOAuthApi) -> None:
        self.db = db
        self.calendar_creator = CalendarCreator(calendar_api)

    def update(self, team: EspnTeam, use_mapper: bool):
        data = team.to_fire_doc()
        doc_ref = self.db.document(f'espn_teams/{team.slug}')
        doc = doc_ref.get()
        if not doc.exists or doc.get('calendar_id') is None:
            print(f'{team.slug} does not have calendar. creating...')
            data['calendar_id'] = self.calendar_creator.create_calendar(team.name, team.flag)
        data['use_mapper'] = use_mapper
        doc_ref.set(data, merge=True)