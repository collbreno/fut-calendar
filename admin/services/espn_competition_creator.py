
from google.cloud.firestore import Client
from services.calendar_api import CalendarOAuthApi
from services.espn_competition_scraper import EspnCompetitionScraper
from services.espn_team_creator import EspnTeamCreator
from services.calendar_creator import CalendarCreator
import json
from models.espn_team import EspnTeam

class EspnCompetitionCreator:
    def __init__(self, db: Client, calendar_api: CalendarOAuthApi) -> None:
        self.db = db
        self.team_creator = EspnTeamCreator(db, calendar_api)
        self.calendar_creator = CalendarCreator(calendar_api)
        self.scraper = EspnCompetitionScraper()

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
                data['calendar_id'] = self.calendar_creator.create_calendar(competition.name, flag)
            else:
                print(f'{slug} already has calendar!')
        if create_teams:
            teams = self.scraper.get_teams(league_slug=slug, flag=flag)
            data['teams'] = list(map(lambda x: self.db.document(f'espn_teams/{x.slug}'), teams))
            self.__update_teams(teams, use_mapper)
        if create_maps:
            self.__update_maps(competition.slug, ['en', 'pt'])
        doc_ref.set(data, merge=True)

    def __update_teams(self, teams: list[EspnTeam], use_mapper: bool):
        for team in teams:
            self.team_creator.update(team, use_mapper)

    def __update_maps(self, slug: str, langs: list[str]):
        with open(f'./map_flags/{slug}.json', encoding='utf-8') as f:
            flag_mapper = json.load(f)
            self.db.document(f'mappers/flag').set(flag_mapper, merge=True)
        for lang in langs:
            lang_mapper = self.scraper.get_map_name(slug, lang)
            self.db.document(f'mappers/lang_{lang}').set(lang_mapper, merge=True)




    