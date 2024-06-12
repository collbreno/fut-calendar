import firebase_admin
from firebase_admin import firestore
from google.cloud.firestore import DocumentReference
from jinja2 import Environment, FileSystemLoader
from dataclasses import dataclass, asdict
import os

DIST_FOLDER = 'dist/'
TEAMS_FOLDER = DIST_FOLDER+'teams/'

@dataclass
class Item:
    image_url: str
    name: str
    link: str
    id: str = ''

def __get_calendar_url(calendar_id: str) -> str:
    return f'https://calendar.google.com/calendar/u/0/r?cid={calendar_id}'

def __get_image_url(soccerway_id: str) -> str :
    return f'https://secure.cache.images.core.optasports.com/soccer/teams/150x150/{soccerway_id}.png'


def __generate_teams_html(competition_name, refs: list[DocumentReference], path):
    teams = []
    for team_ref in refs:
        doc = team_ref.get().to_dict()
        name = doc['name']
        if doc.get('flag') is not None:
            name += f' ({doc.get('flag')})'
        teams.append(asdict(Item(
            name=name,
            image_url=doc.get('image_url', __get_image_url(team_ref.id)),
            link=__get_calendar_url(doc['calendar_id']),
            id=team_ref.id
        )))
    teams.sort(key=lambda x: x['name'])
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template_teams.html')
    html_output = template.render(list=teams, competition=competition_name)

    # Write HTML output to a file
    with open(f'{TEAMS_FOLDER}{path}.html', 'w', encoding='utf-8') as file:
        file.write(html_output)


if __name__ == '__main__':
    firebase_admin.initialize_app()
    db = firestore.client()

    espn_competitions = []
    sw_competitions = []

    if not os.path.exists(TEAMS_FOLDER):
        os.mkdir(TEAMS_FOLDER)

    all_teams = 'Todos os times'
    sw_competitions.append(asdict(Item(
        link='/teams/all',
        name=all_teams,
        image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Soccerball.svg/2048px-Soccerball.svg.png',
    )))
    team_refs: list[DocumentReference] = db.collection('teams').list_documents()
    __generate_teams_html(all_teams, team_refs, 'all')

    competitions: list[DocumentReference] = list(db.collection('competitions').list_documents())

    for competition_ref in competitions:
        competition = competition_ref.get().to_dict()
        if 'teams' in competition:
            sw_competitions.append(asdict(Item(
                link=f'/teams/{competition_ref.id}',
                name=competition['name'],
                image_url=competition['image_url'],
                id=competition_ref.id,
            )))
            __generate_teams_html(competition['name'], competition['teams'], competition_ref.id)
        else:
            espn_competitions.append(asdict(Item(
                link=__get_calendar_url(competition['calendar_id']),
                name=competition['name'],
                image_url=competition['image_url'],
                id=competition_ref.id,
            )))


    env = Environment(loader=FileSystemLoader('.'))
    competitions_template = env.get_template('template_competitions.html')
    html_output = competitions_template.render(
        sw_competitions=sw_competitions, 
        espn_competitions=espn_competitions,
    )

    with open(DIST_FOLDER+'index.html', 'w', encoding='utf-8') as file:
        file.write(html_output)
