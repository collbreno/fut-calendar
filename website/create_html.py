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

def __get_calendar_url(calendar_id: str) -> str:
    return f'https://calendar.google.com/calendar/u/0/r?cid={calendar_id}'

def __get_image_url(soccerway_id: str) -> str :
    return f'https://secure.cache.images.core.optasports.com/soccer/teams/150x150/{soccerway_id}.png'


def __generate_teams_html(refs: list[DocumentReference], path):
    team_data = []
    for team_ref in refs:
        doc = team_ref.get().to_dict()
        name = doc['name']
        if doc.get('flag') is not None:
            name += f' ({doc.get('flag')})'
        team_data.append({
            'name': name,
            'image_url':doc.get('image_url', __get_image_url(team_ref.id)),
            'link': __get_calendar_url(doc['calendar_id'])
        })
    team_data.sort(key=lambda x: x['name'])
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template_teams.html')
    html_output = template.render(list=team_data)

    # Write HTML output to a file
    with open(f'{TEAMS_FOLDER}{path}.html', 'w', encoding='utf-8') as file:
        file.write(html_output)


if __name__ == '__main__':
    firebase_admin.initialize_app()
    db = firestore.client()


    competition_data = []

    if not os.path.exists(TEAMS_FOLDER):
        os.mkdir(TEAMS_FOLDER)

    competition_data.append(asdict(Item(
        link='/teams/all',
        name='Todos os times',
        image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Soccerball.svg/2048px-Soccerball.svg.png'
    )))
    teams: list[DocumentReference] = db.collection('teams').list_documents()
    __generate_teams_html(teams, 'all')

    competitions: list[DocumentReference] = list(db.collection('competitions').list_documents())

    for competition_ref in competitions:
        competition = competition_ref.get().to_dict()
        competition_data.append(asdict(Item(
            link=f'/teams/{competition_ref.id}',
            name=competition['name'],
            image_url=competition['image_url']
        )))
        __generate_teams_html(competition['teams'], competition_ref.id)


    env = Environment(loader=FileSystemLoader('.'))
    competitions_template = env.get_template('template_competitions.html')
    html_output = competitions_template.render(list=competition_data)

    with open(DIST_FOLDER+'index.html', 'w', encoding='utf-8') as file:
        file.write(html_output)
