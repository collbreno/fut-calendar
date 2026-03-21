from services.espn_competition_creator import EspnCompetitionCreator
from services.calendar_api import CalendarOAuthApi
from firebase_admin import firestore, initialize_app
import os

if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './python_admin_credentials.json'
    initialize_app()
    db = firestore.client()
    calendar_api = CalendarOAuthApi()
    creator = EspnCompetitionCreator(db=db, calendar_api=calendar_api)
    creator.update(
        slug='fifa.world', 
        create_calendar=True,
        create_teams=False, 
        create_maps=True,
        use_mapper=True,
        flag=None, 
    )
    # creator.update('uefa.euro')