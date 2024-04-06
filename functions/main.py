# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
from firebase_functions.firestore_fn import (
    on_document_written,
    Event,
    Change,
    DocumentSnapshot,
)

from firebase_functions import (
    https_fn,
    options,
    pubsub_fn,
)

# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app, firestore
from google.cloud.firestore import Client
from calendar_api import CalendarAPI
from datetime import datetime

app = initialize_app()

# @https_fn.on_request(
#     cors=options.CorsOptions(
#         cors_origins="*",
#         cors_methods=["post"],
#     )
# )
# def run_scraper(req: https_fn.Request) -> https_fn.Response:
#     if 'team_id' in req.args:
#         print(f'team_id encontrado! {req.args['team_id']}')
#     else:
#         print('team_id não encontrado!')

#     return https_fn.Response('Finished!')

@pubsub_fn.on_message_published(topic='run-all-scrapers')
def run_all(event: pubsub_fn.CloudEvent[pubsub_fn.MessagePublishedData]):
    client: Client = firestore.client()
    teams: list[DocumentSnapshot] = client.collection('teams').get()
    for team in teams:
        client.document(f'teams/{team.id}').update({
            'last_update': datetime.now()
        })


@on_document_written(document='teams/{team}/matches/{matchId}')
def write_to_calendar(event: Event[Change[DocumentSnapshot]]) -> None:
    match_id = event.params['matchId']
    team = event.params['team']

    print('Printando credenciais...')
    print(app.credential)
    print(app.credential.get_credential())
    print('-------------------------')

    client: Client = firestore.client()
    teamDoc = client.document(f'teams/{team}').get()
    calendar_id = teamDoc.to_dict()['calendar_id']

    calendar_event = {
        'id': match_id,
        'summary': 'Partida teste',
        'start': {
            'dateTime': '2024-04-05T16:00:00',
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': '2024-04-05T18:00:00',
            'timeZone': 'America/Sao_Paulo',
        }
    }


    if event.data.after is not None:
        print(f'teams/{team}/matches/{match_id} criado ou atualizado')
        document = event.data.after.to_dict()
        print(document)
        calendar_api = CalendarAPI(None)
        calendar_api.upsert(calendar_id=calendar_id, event=calendar_event)
    else:
        print('Objeto excluido')
    