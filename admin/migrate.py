from firebase_admin import firestore, initialize_app
from services.migrator import Migrator
from google.cloud.firestore import CollectionReference, DocumentReference, Client

if __name__ == '__main__':
    initialize_app()
    db = firestore.client()
    migrator = Migrator(db)
    teams: list[DocumentReference] = list(db.collection('teams').list_documents())
    for team in teams:
        if not str(team.id)[0].isdigit():
            soccerway_id = team.get().to_dict()['soccerway_id']
            new_path = team.path.replace(team.id, soccerway_id)
            migrator.migrate(team.path, new_path)
            print(f'{team.path} >>> {new_path}')