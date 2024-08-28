from firebase_admin import firestore, initialize_app
from services.espn_migrator import EspnMigrator
from services.espn_team_scraper import EspnTeamScraper
from services.espn_competition_scraper import EspnCompetitionScraper
from services.calendar_api import CalendarOAuthApi
from models.espn_team import EspnTeam

import json

def __load_mapper() -> dict:
    with open('espn_to_soccerway.json', encoding='utf-8') as f:
        return json.load(f)

if __name__ == '__main__':
    initialize_app()
    db = firestore.client()
    calendar_api = CalendarOAuthApi()
    team_scraper = EspnTeamScraper()
    competition_scraper = EspnCompetitionScraper()
    migrator = EspnMigrator(db, calendar_api)
    sw_id_mapper = __load_mapper()

    # teams = competition_scraper.get_teams('fra.1', flag=None)
    teams: list[EspnTeam] = []
    # teams.append(team_scraper.get('191')) # SJ
    # teams.append(team_scraper.get('2674')) # Santos FC
    teams.append(team_scraper.get('22187', flag='Fem')) # Bay FC
    for team in teams:
        if team.slug in sw_id_mapper:
            sw_id = sw_id_mapper[team.slug]

            # migrator.migrate(team, sw_id)
            
            # if db.document(f'teams/{sw_id}').get().exists:
            #     deleted = 0
            #     docs = db.collection(f'teams/{sw_id}/matches').list_documents()
            #     for doc in docs:
            #         doc.delete()
            #         deleted += 1
            #     print(f'Deleted from {team.slug}: {deleted} matches')

            db.document(f'teams/{sw_id}').delete()
            print(f'Deleted sw:{sw_id} ({team.slug}) from database')
        else:
            print(f'{team.slug} not in soccerway mapper')






