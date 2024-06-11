
from google.cloud.firestore import Client
from services.calendar_api import CalendarOAuthApi
from services.espn_competition_scraper import EspnCompetitionScraper

class EspnCompetitionCreator:
    def __init__(self,db: Client, calendar_api: CalendarOAuthApi) -> None:
        self.db = db
        self.calendar_api = calendar_api
        self.scraper = EspnCompetitionScraper()

    def __get_calendar_name(self, team_name, flag: str):
        name = f'Jogos {team_name}'        
        if flag is not None and len(flag) > 0:
            name += f' {flag}'
        return name

    def update(self, slug: str, flag: str = None):
        competition = self.scraper.get(slug)
        data = {
            'image_url': competition.logo,
            'name': competition.name,
            'flag': flag,
        }

        doc_ref = self.db.document(f'competitions/{competition.slug}')
        doc = doc_ref.get()
        if not doc.exists or doc.get('calendar_id') is None:
            print(f'{slug} does not have calendar. creating...')
            calendar_id = self.calendar_api.create_calendar(self.__get_calendar_name(competition.name, flag))
            self.calendar_api.make_public(calendar_id)
            self.calendar_api.add_as_writer(calendar_id, '156268949150-compute@developer.gserviceaccount.com')
            data['calendar_id'] = calendar_id
        else:
            print(f'{slug} already has calendar!')
        doc_ref.set(data, merge=True)


    