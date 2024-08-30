import firebase_admin
from firebase_admin import firestore
from google.cloud.firestore import DocumentReference
from jinja2 import Environment, FileSystemLoader
from dataclasses import dataclass, asdict
import os

@dataclass
class Item:
    image_url: str
    name: str
    link: str
    id: str = ''

def __get_calendar_url(calendar_id: str) -> str:
    return f'https://calendar.google.com/calendar/u/0/r?cid={calendar_id}'

# def __sort_competitions(competitions: list[dict]):
#     new_list = []
#     for c in competitions:
#         if c['id'] == 'conmebol.america':
#             new_list.append(c)
#     for c in competitions:
#         if c['id'] == 'uefa.euro':
#             new_list.append(c)
#     for c in competitions:
#         if c['id'] != 'uefa.euro' and c['id'] != 'conmebol.america':
#             new_list.append(c)
#     return new_list

def __generate_teams_html(item: Item, refs: list[DocumentReference]):
    teams = []
    for team_ref in refs:
        doc = team_ref.get().to_dict()
        name = doc['name']
        flag = doc.get('flag')
        if flag is not None and len(flag) > 0:
            name += f' ({flag})'
        teams.append(asdict(Item(
            name=name,
            image_url=doc.get('image_url'),
            link=__get_calendar_url(doc['calendar_id']),
            id=team_ref.id
        )))
    teams.sort(key=lambda x: x['name'])
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template_teams.html')
    html_output = template.render(list=teams, competition_name=item.name)

    # Write HTML output to a file
    with open(f'dist{item.link}.html', 'w', encoding='utf-8') as file:
        file.write(html_output)


if __name__ == '__main__':
    firebase_admin.initialize_app()
    db = firestore.client()

    competition_calendars = []
    competitions = []

    if not os.path.exists('dist/teams'):
        os.mkdir('dist/teams')

    all_teams = Item(
        id='all',
        link='/teams/all',
        name='Todos os Times e Seleções',
        image_url='https://png.pngtree.com/png-vector/20221206/ourmid/pngtree-world-earth-logo-vector-design-png-image_6514310.png',
    )
    competitions.append(all_teams)
    team_refs: list[DocumentReference] = db.collection('espn_teams').list_documents()
    __generate_teams_html(all_teams, team_refs)

    competition_refs: list[DocumentReference] = list(db.collection('competitions').list_documents())

    for competition_ref in competition_refs:
        competition = competition_ref.get().to_dict()
        if 'teams' in competition:
            item = Item(
                link=f'/teams/{competition_ref.id}',
                name=competition['name'],
                image_url=competition['image_url'],
                id=competition_ref.id,
            )
            competitions.append(item)
            __generate_teams_html(item, competition['teams'])
        if 'calendar_id' in competition and not competition.get('disabled', False):
            competition_calendars.append(Item(
                link=__get_calendar_url(competition['calendar_id']),
                name=competition['name'],
                image_url=competition['image_url'],
                id=competition_ref.id,
            ))


    env = Environment(loader=FileSystemLoader('.'))
    competitions_template = env.get_template('template_index.html')
    html_output = competitions_template.render(
        competition_calendars=list(map(asdict, competition_calendars)), 
        competitions=list(map(asdict, competitions)),
    )

    with open('dist/index.html', 'w', encoding='utf-8') as file:
        file.write(html_output)
