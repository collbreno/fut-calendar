from firebase_functions.firestore_fn import on_document_written, on_document_updated, Event, Change, DocumentSnapshot
from firebase_functions import https_fn, tasks_fn, pubsub_fn, logger
from firebase_functions.options import RetryConfig, RateLimits, SupportedRegion
from firebase_admin import initialize_app, firestore, functions
from google.cloud.firestore import Client
from services.calendar_api import CalendarAPI
from services.match_converter import MatchConverter
from datetime import datetime
from services.matches_scraper import MatchesScraper
from dataclasses import asdict
from models.match import Match
from utils.calendar_utils import CalendarUtils
import google.auth
from google.auth.transport.requests import AuthorizedSession

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

@on_document_written(document='teams/{team}')
def run_scraper(event: Event[Change[DocumentSnapshot]]) -> https_fn.Response:
    team = event.params['team']
    tag = f'[{team}]'
    after = event.data.after
    if after is not None:
        doc = after.to_dict()
        if event.data.before is not None and event.data.before.to_dict().get('last_update') == doc.get('last_update'):
            logger.debug(f'{tag} last_update did not changed finishing execution...')
            return
        
        if doc.get('calendar_id') is None:
            logger.debug(f'{tag} team does not have calendar id')
            return
        
        client: Client = firestore.client()
        scraper = MatchesScraper(soccerway_id=team, flag=doc['flag'])
        matches = list(scraper.get_scheduled_matches())
        for match in matches:
            client.document(f'teams/{team}/matches/{match.id}').set(
                asdict(match)
            )
            logger.info(f'{tag} set match {match.id} ({match.home} x {match.away})')
        to_delete = list(scraper.get_cancelled_match_ids())
        for id_to_delete in to_delete:
            doc_ref = client.document(f'teams/{team}/matches/{id_to_delete}')
            if doc_ref.get().exists:
                doc_ref.delete()
                logger.info(f'{tag} delete match {id_to_delete}')

@on_document_written(document='teams/{team}/matches/{match}')
def enque_calendar_writer_task(event: Event[Change[DocumentSnapshot]]):
    team = event.params['team']
    match_id = event.params['match']
    tag = f'[{team}/{match_id}]'
    logger.debug(f'{tag} cloud function started')


    client: Client = firestore.client()
    teamDoc = client.document(f'teams/{team}').get()
    calendar_id = teamDoc.to_dict().get('calendar_id')

    if calendar_id is None:
        logger.error(f'{tag} team does not have calendar id')
        return

    converter = MatchConverter()
    after = event.data.after

    if after is not None:
        before = event.data.before
        document = after.to_dict()
        if before is None or before.to_dict() != document:
            task_queue = functions.task_queue('insertCalendarEvent')
            target_uri = __get_function_url('insertCalendarEvent')
            calendar_event = converter.convert(Match(**document))
            body = {'data': {'calendar_id': calendar_id, 'event': calendar_event}}
            task_options = functions.TaskOptions(uri=target_uri)
            task_queue.enqueue(body, task_options)
            logger.debug(f'{tag} task to insert enqued!')
        else:
            logger.debug(f'{tag} match did not changed')
    else:
        task_queue = functions.task_queue('deleteCalendarEvent')
        target_uri = __get_function_url('deleteCalendarEvent')
        body = {'data': {'calendar_id': calendar_id, 'event_id': CalendarUtils.format_id(match_id)}}
        task_options = functions.TaskOptions(uri=target_uri)
        task_queue.enqueue(body, task_options)
        logger.debug(f'{tag} task to delete enqued!')


@tasks_fn.on_task_dispatched(retry_config=RetryConfig(max_attempts=3, min_backoff_seconds=60), rate_limits=RateLimits(max_dispatches_per_second=50))
def insertCalendarEvent(req: tasks_fn.CallableRequest):
    calendar_id = req.data['calendar_id']
    event = req.data['event']
    calendar_api = CalendarAPI()
    calendar_api.upsert(calendar_id=calendar_id, event=event)
    logger.debug(f'[{calendar_id}/{event['id']}] event updated!')

@tasks_fn.on_task_dispatched(retry_config=RetryConfig(max_attempts=3, min_backoff_seconds=60), rate_limits=RateLimits(max_dispatches_per_second=50))
def deleteCalendarEvent(req: tasks_fn.CallableRequest):
    calendar_id = req.data['calendar_id']
    event_id = req.data['event_id']
    calendar_api = CalendarAPI()
    calendar_api.delete(calendar_id=calendar_id, event_id=event_id)
    logger.debug(f'[{calendar_id}/{event_id}] event deleted!')


def __get_function_url(name: str) -> str:
    credentials, project_id = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"])
    authed_session = AuthorizedSession(credentials)
    url = ("https://cloudfunctions.googleapis.com/v2beta/" +
           f"projects/{project_id}/locations/us-central1/functions/{name}")
    logger.debug(f'url: {url}')
    response = authed_session.get(url)
    data = response.json()
    logger.debug('getting function url')
    logger.debug(data)
    function_url = data["serviceConfig"]["uri"]
    return function_url