import json
from services.calendar_api import CalendarAPI
from constants import LOCAL_TIME_ZONE, WOMEN_FLAG
from scrapers.team_scraper import TeamScraper
from unidecode import unidecode
import os

def __format_filename(text: str):
    return unidecode(text.lower()).replace(' ', '_')+'.json'

def __mount_calendar(summary: str):
    return {
        'summary': summary,
        'timeZone': LOCAL_TIME_ZONE
    }

def create_all():
    folder = './teams/'
    scraper = TeamScraper()
    calendar_api = CalendarAPI()

    with open('teams.txt') as file:
        for team_url in file:
            data = scraper.get_info(team_url)
            team = data['team']
            
            if ('women' in team_url):
                team = f'{team} {WOMEN_FLAG}'
                data['flag'] = WOMEN_FLAG

            json_filename = __format_filename(team)

            if os.path.exists(f'{folder}{json_filename}'):
                print(f'{team} already added.')
            else:
                print(f'Creating settings for {team}...')
                calendar = __mount_calendar(f'Jogos {team}')
                data['calendar_id'] = calendar_api.create_calendar(calendar)
                calendar_api.make_public(data['calendar_id'])

                json_object = json.dumps(data)

                with open(f'{folder}{json_filename}', 'w') as json_file:
                    json_file.write(json_object)