from services.competition_scraper import CompetitionScraper
from services.calendar_api import CalendarOAuthApi
from services.team_creator import TeamCreator
from firebase_admin import firestore, initialize_app

class CompetitionCreator:
    def __init__(self) -> None:
        initialize_app()
        self.db = firestore.client()
        self.competition_scraper = CompetitionScraper()
        self.team_creator = TeamCreator(self.db, CalendarOAuthApi())

    def update(self, competition_url, flag = None):
        competition = self.competition_scraper.get(competition_url)
        self.db.collection('competitions').document(competition.id).set({
            'teams': list(map(lambda x: self.db.document(f'teams/{x}'), competition.teams)),
            'name': competition.name
        })
        for team in competition.teams:
            self.team_creator.update(team, flag)