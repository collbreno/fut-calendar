
from google.cloud.firestore import Client
from services.calendar_api import CalendarOAuthApi
from services.espn_competition_scraper import EspnCompetitionScraper
import json
from models.espn_team import EspnTeam

class EspnCompetitionCreator:
    def __init__(self, db: Client, calendar_api: CalendarOAuthApi) -> None:
        self.db = db
        self.calendar_api = calendar_api
        self.scraper = EspnCompetitionScraper()

    def __get_calendar_name(self, team_name, flag: str):
        name = f'Jogos {team_name}'        
        if flag is not None and len(flag) > 0:
            name += f' {flag}'
        return name

    def update(self, slug: str, flag: str, create_calendar: bool, create_teams: bool, use_mapper: bool, create_maps: bool):
        competition = self.scraper.get(slug)
        data = {
            'image_url': competition.logo,
            'name': competition.name,
            'flag': flag,
            'use_mapper': use_mapper,
        }

        doc_ref = self.db.document(f'competitions/{competition.slug}')
        doc = doc_ref.get()
        if create_calendar:
            if not doc.exists or doc.get('calendar_id') is None:
                print(f'{slug} does not have calendar. creating...')
                calendar_id = self.calendar_api.create_calendar(self.__get_calendar_name(competition.name, flag))
                self.calendar_api.make_public(calendar_id)
                self.calendar_api.add_as_writer(calendar_id, '156268949150-compute@developer.gserviceaccount.com')
                data['calendar_id'] = calendar_id
            else:
                print(f'{slug} already has calendar!')
        if create_teams:
            teams = self.scraper.get_teams(league_slug=slug, flag=flag)
            print(type(teams))
            print(len(teams))
            data['teams'] = list(map(lambda x: self.db.document(f'espn_teams/{x.slug}'), teams))
            self.__create_teams(teams, flag, use_mapper)
        if create_maps:
            self.__update_maps(competition.slug, ['en', 'pt'])
        doc_ref.set(data, merge=True)

    def __create_teams(self, teams: list[EspnTeam], flag, use_mapper):
        for team in teams:
            data = team.to_fire_doc()
            doc_ref = self.db.document(f'espn_teams/{team.slug}')
            doc = doc_ref.get()
            if not doc.exists or doc.get('calendar_id') is None:
                print(f'{team.slug} does not have calendar. creating...')
                calendar_id = self.calendar_api.create_calendar(self.__get_calendar_name(team.name, flag))
                self.calendar_api.make_public(calendar_id)
                self.calendar_api.add_as_writer(calendar_id, '156268949150-compute@developer.gserviceaccount.com')
                data['calendar_id'] = calendar_id
            data['use_mapper'] = use_mapper
            doc_ref.set(data, merge=True)

    def __update_maps(self, slug: str, langs: list[str]):
        with open(f'./map_flags/{slug}.json', encoding='utf-8') as f:
            flag_mapper = json.load(f)
            self.db.document(f'mappers/flag').set(flag_mapper, merge=True)
        for lang in langs:
            lang_mapper = self.scraper.get_map_name(slug, lang)
            self.db.document(f'mappers/lang_{lang}').set(lang_mapper, merge=True)




    