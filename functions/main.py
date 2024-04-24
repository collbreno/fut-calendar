# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
from firebase_functions.firestore_fn import (
    on_document_written,
    on_document_updated,
    Event,
    Change,
    DocumentSnapshot,
)

from firebase_functions import (
    https_fn,
    pubsub_fn,
    logger,
)

# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app, firestore
from google.cloud.firestore import Client
from services.calendar_api import CalendarAPI
from services.match_converter import MatchConverter
from datetime import datetime
from services.matches_scraper import MatchesScraper
from dataclasses import asdict
from models.match import Match
from utils.calendar_utils import CalendarUtils

app = initialize_app()

@pubsub_fn.on_message_published(topic='run-all-scrapers')
def run_all(event: pubsub_fn.CloudEvent[pubsub_fn.MessagePublishedData]):
    client: Client = firestore.client()
    teams: list[DocumentSnapshot] = client.collection('teams').get()
    for team in teams:
        client.document(f'teams/{team.id}').update({
            'last_update': datetime.now()
        })
        logger.info(f'{team.id} updated!')

@on_document_updated(document='teams/{team}')
def run_scraper(event: Event[Change[DocumentSnapshot]]) -> https_fn.Response:
    team = event.params['team']
    tag = f'[{team}]'
    doc = event.data.after.to_dict()
    if event.data.before.to_dict().get('last_update') == doc.get('last_update'):
        logger.debug(f'{tag} last_update did not changed finishing execution...')
        return
    
    client: Client = firestore.client()
    scraper = MatchesScraper(soccerway_id=doc['soccerway_id'], flag=doc['flag'])
    matches = list(scraper.get_scheduled_matches())
    for match in matches:
        client.document(f'teams/{team}/matches/{match.id}').set(
            asdict(match)
        )
        logger.info(f'{tag} set match {match.id} ({match.home} x {match.away})')
    

@on_document_written(document='teams/{team}/matches/{matchId}')
def write_to_calendar(event: Event[Change[DocumentSnapshot]]) -> None:
    team = event.params['team']
    match_id = event.params['matchId']
    tag = f'[{team}/{match_id}]'
    logger.debug(f'{tag} function started!')

    client: Client = firestore.client()
    teamDoc = client.document(f'teams/{team}').get()
    calendar_id = teamDoc.to_dict()['calendar_id']
    converter = MatchConverter()

    after = event.data.after
    calendar_api = CalendarAPI()

    if after is not None:
        before = event.data.before
        document = after.to_dict()
        if before is None or before.to_dict() != document:
            calendar_event = converter.convert(Match(**document))
            calendar_api.upsert(calendar_id=calendar_id, event=calendar_event)
            logger.info(f'{tag} match updated!')
        else:
            logger.debug(f'{tag} match did not changed')
    else:
        calendar_api.delete(
            calendar_id=calendar_id, 
            event_id=CalendarUtils.format_id(match_id)
        )
        logger.debug(f'{tag} match deleted!')
    