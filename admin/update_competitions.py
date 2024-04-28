from services.competition_creator import CompetitionCreator
from firebase_admin import firestore, initialize_app


if __name__ == '__main__':
    creator = CompetitionCreator()
    # creator.update('https://br.soccerway.com/national/brazil/serie-a/2024')
    # creator.update('https://br.soccerway.com/national/united-states/mls/2024')
    # creator.update('https://br.soccerway.com/national/england/premier-league/20232024')

