from firebase_functions.firestore_fn import on_document_written, on_document_updated, Event, Change, DocumentSnapshot
from firebase_functions import https_fn, tasks_fn, pubsub_fn, logger
from firebase_functions.options import RetryConfig, RateLimits, SupportedRegion
from firebase_admin import initialize_app, firestore, functions
from google.cloud.firestore import Client
from services.calendar_api import CalendarAPI
from services.match_converter import MatchConverter
from datetime import datetime
from services.matches_scraper import MatchesScraper
from services.espn_competition_scraper import EspnCompetitionScraper
from services.espn_team_scraper import EspnTeamScraper
from dataclasses import asdict
from models.match import Match
from utils.calendar_utils import CalendarUtils
import google.auth
from google.auth.transport.requests import AuthorizedSession
from services.teams_mapper import TeamsMapper

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
    competitions: list[DocumentSnapshot] = client.collection('competitions').get()
    for competition in competitions:
        client.document(f'competitions/{competition.id}').update({
            'last_update': datetime.now()
        })
        logger.info(f'{competition.id} updated!')

@on_document_written(document='teams/{team}')
def run_scraper(event: Event[Change[DocumentSnapshot]]) -> https_fn.Response:
    team = event.params['team']
    tag = f'[{team}]'
    after = event.data.after
    if after is not None:
        doc = after.to_dict()
        if event.data.before is not None and event.data.before.to_dict().get('last_update') == doc.get('last_update'):
            logger.debug(f'{tag} last_update did not changed. finishing execution...')
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

@on_document_written(document='competitions/{league_slug}')
def runCompetitionScraper(event: Event[Change[DocumentSnapshot]]) -> https_fn.Response:
    league_slug = event.params['league_slug']
    tag = f'[{league_slug}]'
    after = event.data.after
    if after is not None:
        doc = after.to_dict()
        if event.data.before is not None and event.data.before.to_dict().get('last_update') == doc.get('last_update'):
            logger.debug(f'{tag} last_update did not changed. finishing execution...')
            return
        
        if doc.get('calendar_id') is None:
            logger.debug(f'{tag} does not have calendar id')
            return
        
        client: Client = firestore.client()
        mapper = None
        if doc.get('use_mapper') == True:
            flag_mapper = client.document('mappers/flag').get().to_dict()
            pt_mapper = client.document('mappers/lang_en').get().to_dict()
            en_mapper = client.document('mappers/lang_pt').get().to_dict()
            mapper = TeamsMapper(map_flag=flag_mapper, map_langs=[pt_mapper, en_mapper])
        scraper = EspnCompetitionScraper(league_slug=league_slug, flag=doc['flag'],mapper=mapper)
        matches = list(scraper.get_scheduled_matches())
        for match in matches:
            client.document(f'competitions/{league_slug}/matches/{match.id}').set(
                asdict(match)
            )
            logger.info(f'{tag} set match {match.id} ({match.home} x {match.away})')
        # to_delete = list(scraper.get_cancelled_match_ids())
        # for id_to_delete in to_delete:
        #     doc_ref = client.document(f'competitions/{league_slug}/matches/{id_to_delete}')
        #     if doc_ref.get().exists:
        #         doc_ref.delete()
        #         logger.info(f'{tag} delete match {id_to_delete}')

@on_document_written(document='espn_teams/{team_slug}')
def runEspnTeamScraper(event: Event[Change[DocumentSnapshot]]) -> https_fn.Response:
    team_slug = event.params['team_slug']
    tag = f'[{team_slug}]'
    after = event.data.after
    if after is not None:
        doc = after.to_dict()
        if event.data.before is not None and event.data.before.to_dict().get('last_update') == doc.get('last_update'):
            logger.debug(f'{tag} last_update did not changed. finishing execution...')
            return
        
        if doc.get('calendar_id') is None:
            logger.debug(f'{tag} does not have calendar id')
            return
        
        client: Client = firestore.client()
        mapper = None
        if doc.get('use_mapper') == True:
            flag_mapper = client.document('mappers/flag').get().to_dict()
            pt_mapper = client.document('mappers/lang_en').get().to_dict()
            en_mapper = client.document('mappers/lang_pt').get().to_dict()
            mapper = TeamsMapper(map_flag=flag_mapper, map_langs=[pt_mapper, en_mapper])
        scraper = EspnTeamScraper(team_id=doc['id'], mapper=mapper, flag=doc.get('flag'))
        matches = list(scraper.get_scheduled_matches())
        for match in matches:
            client.document(f'espn_teams/{team_slug}/matches/{match.id}').set(
                asdict(match)
            )
            logger.info(f'{tag} set match {match.id} ({match.home} x {match.away})')
        # to_delete = list(scraper.get_cancelled_match_ids())
        # for id_to_delete in to_delete:
        #     doc_ref = client.document(f'espn_teams/{team_slug}/matches/{id_to_delete}')
        #     if doc_ref.get().exists:
        #         doc_ref.delete()
        #         logger.info(f'{tag} delete match {id_to_delete}')

@on_document_written(document='teams/{team}/matches/{match}')
def onTeamMatchWritten(event: Event[Change[DocumentSnapshot]]):
    team = event.params['team']
    match_id = event.params['match']
    tag = f'[{team}/{match_id}]'
    logger.debug(f'{tag} cloud function started')
    client: Client = firestore.client()
    teamDoc = client.document(f'teams/{team}').get()
    calendar_id = teamDoc.to_dict().get('calendar_id')
    __enqueCalendarWriterTask(
        calendar_id=calendar_id,
        tag=tag,
        match_id=match_id,
        data=event.data,
    )

@on_document_written(document='espn_teams/{team}/matches/{match}')
def onEspnTeamMatchWritten(event: Event[Change[DocumentSnapshot]]):
    team = event.params['team']
    match_id = event.params['match']
    tag = f'[{team}/{match_id}]'
    logger.debug(f'{tag} cloud function started')
    client: Client = firestore.client()
    teamDoc = client.document(f'espn_teams/{team}').get()
    calendar_id = teamDoc.to_dict().get('calendar_id')
    __enqueCalendarWriterTask(
        calendar_id=calendar_id,
        tag=tag,
        match_id=match_id,
        data=event.data,
    )

@on_document_written(document='competitions/{slug}/matches/{match}')
def onCompetitionMatchWritten(event: Event[Change[DocumentSnapshot]]):
    slug = event.params['slug']
    match_id = event.params['match']
    tag = f'[{slug}/{match_id}]'
    logger.debug(f'{tag} cloud function started')
    client: Client = firestore.client()
    competitionDoc = client.document(f'competitions/{slug}').get()
    calendar_id = competitionDoc.to_dict().get('calendar_id')
    __enqueCalendarWriterTask(
        calendar_id=calendar_id,
        tag=tag,
        match_id=match_id,
        data=event.data,
    )

def __enqueCalendarWriterTask(calendar_id: str, match_id: str, tag: str, data: Change[DocumentSnapshot]):
    if calendar_id is None:
        logger.error(f'{tag} does not have calendar id')
        return

    converter = MatchConverter()
    after = data.after

    if after is not None:
        before = data.before
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