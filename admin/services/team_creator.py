from services.team_scraper import TeamScraper
from firebase_admin.firestore import firestore
from google.cloud.firestore import Client
from services.calendar_api import CalendarOAuthApi
from datetime import datetime

class TeamCreator:
    def __init__(self, db: Client, calendar_api: CalendarOAuthApi) -> None:
        self.scraper = TeamScraper()
        self.db = db
        self.calendar_api = calendar_api

    def __get_calendar_name(self, team_name, flag: str):
        name = f'Jogos {team_name}'        
        if flag is not None and len(flag) > 0:
            name += f' {flag}'
        return name
    
    def update(self, team_id: str, flag: str = None):
        name = self.scraper.get_name(team_id)
        data = {
            'soccerway_id': firestore.DELETE_FIELD,
            'name': name,
            'flag': flag,
            'last_update': datetime.now()
        }
        doc_ref = self.db.document(f'teams/{team_id}')
        doc = doc_ref.get()
        if not doc.exists or doc.get('calendar_id') is None:
            print(f'{name} does not have calendar. creating...')
            calendar_id = self.calendar_api.create_calendar(self.__get_calendar_name(name, flag))
            self.calendar_api.make_public(calendar_id)
            self.calendar_api.add_as_writer(calendar_id, '156268949150-compute@developer.gserviceaccount.com')
            data['calendar_id'] = calendar_id
        else:
            print(f'{name} already has calendar!')
        doc_ref.set(data, merge=True)

