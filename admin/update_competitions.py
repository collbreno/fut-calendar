from services.competition_scraper import CompetitionScraper
from firebase_admin import firestore, initialize_app

class Runner:
    def __init__(self) -> None:
        initialize_app()
        self.db = firestore.client()
        self.scraper = CompetitionScraper()
        
    def update(self, competition_url):
        competition = self.scraper.get(competition_url)
        self.db.collection('competitions').document(competition.id).set({
            'teams': list(map(lambda x: self.db.document(f'teams/{x}'), competition.teams)),
            'name': competition.name
        })

if __name__ == '__main__':
    runner = Runner()
    runner.update('https://br.soccerway.com/national/united-states/mls/2024')
    runner.update('https://br.soccerway.com/national/brazil/serie-a/2024')
    runner.update('https://br.soccerway.com/national/england/premier-league/20232024')

