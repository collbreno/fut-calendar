from services.espn_team_creator import EspnTeamCreator
from services.calendar_api import CalendarOAuthApi
from services.espn_team_scraper import EspnTeamScraper
from firebase_admin import firestore, initialize_app


if __name__ == '__main__':
    initialize_app()
    db = firestore.client()
    calendar_api = CalendarOAuthApi()
    scraper = EspnTeamScraper()
    creator = EspnTeamCreator(db=db, calendar_api=calendar_api)

    abc = scraper.get('9965')
    creator.update(abc, use_mapper=False)