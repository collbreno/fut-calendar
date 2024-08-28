from services.espn_competition_creator import EspnCompetitionCreator
from services.calendar_api import CalendarOAuthApi
from firebase_admin import firestore, initialize_app


if __name__ == '__main__':
    initialize_app()
    db = firestore.client()
    calendar_api = CalendarOAuthApi()
    creator = EspnCompetitionCreator(db=db, calendar_api=calendar_api)
    creator.update(
        slug='fifa.olympics', 
        create_calendar=True,
        create_maps=True,
        create_teams=False, 
        flag='Fem', 
        use_mapper=True,
    )
    # creator.update('uefa.euro')