from google.cloud.firestore import Client
from models.espn_team import EspnTeam
from services.calendar_api import CalendarOAuthApi
from services.calendar_creator import CalendarCreator


class EspnMigrator:
    def __init__(self, db: Client, calendar_api: CalendarOAuthApi) -> None:
        self.db = db
        self.calendar_creator = CalendarCreator(calendar_api)

    def migrate(self, espn_team: EspnTeam, soccerway_id: str):
        espn_doc = self.db.document(f'espn_teams/{espn_team.slug}')
        if espn_doc.get().exists:
            print(f'{espn_team.slug} already exists on firestore database!')
        else:
            sw_doc = self.db.document(f'teams/{soccerway_id}').get()
            data = espn_team.to_fire_doc()
            if sw_doc.exists:
                data['calendar_id'] = sw_doc.to_dict()['calendar_id']
            else: 
                data['calendar_id'] = self.calendar_creator.create_calendar(
                    name=espn_team.name, 
                    flag=espn_team.flag
                )
            data['use_mapper'] = False
            espn_doc.set(data)
            print(f'Added {espn_team.slug} to database!')
