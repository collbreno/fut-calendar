from services.espn_competition_creator import EspnCompetitionCreator
from services.calendar_api import CalendarOAuthApi
from firebase_admin import firestore, initialize_app


if __name__ == '__main__':
    initialize_app()
    db = firestore.client()
    calendar_api = CalendarOAuthApi()
    creator = EspnCompetitionCreator(db=db, calendar_api=calendar_api)
    creator.update('conmebol.america')
    creator.update('uefa.euro')
    creator.update('fifa.olympics')