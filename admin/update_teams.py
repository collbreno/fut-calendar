from firebase_admin import firestore, initialize_app
from services.team_creator import TeamCreator
from services.calendar_api import CalendarOAuthApi

if __name__ == '__main__':
    initialize_app()
    db = firestore.client()
    creator = TeamCreator(db, CalendarOAuthApi())
    # creator.update('2276') # SJ Earthquakes
    # creator.update('5967', 'Fem') # Brasil Fem
    # creator.update('5977', 'Fem') # EUA Fem
    # creator.update('35478', 'Fem') # Corinthians Fem
    # creator.update('4128', 'Fem') # Espanha Fem
    # creator.update('64200', 'Fem') # Bay Fem
    # creator.update('46189', 'Fem') # Fluminense Fem
    # creator.update('24076') # Fluminense u17
    # creator.update('22802') # Fluminense u20
    # creator.update('22827') # Botafogo u20
    # creator.update('21622') # Flamengo u20
    # creator.update('22815') # Vasco u20
    # creator.update('337') # América MG
    # creator.update('660') # Arsenal
    # creator.update('349') # Brasil
    # creator.update('324') # Coritiba
    # creator.update('307') # Goiás
    # creator.update('325') # Santa Cruz
    # creator.update('319') # Santos

    # creator.update('309') # Paraná Club
    # creator.update('6223') # Chapecoense
    # creator.update('1678') # Porto
    # creator.update('962') # Stuttgart


