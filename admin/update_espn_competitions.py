from services.espn_competition_creator import EspnCompetitionCreator
from services.calendar_api import CalendarOAuthApi
from firebase_admin import firestore, initialize_app


if __name__ == '__main__':
    initialize_app()
    db = firestore.client()
    calendar_api = CalendarOAuthApi()
    creator = EspnCompetitionCreator(db=db, calendar_api=calendar_api)
    creator.update(
        slug='bra.1', 
        create_calendar=True,
        create_teams=True, 
        create_maps=False,
        use_mapper=False,
        flag=None, 
    )
    # creator.update('uefa.euro')