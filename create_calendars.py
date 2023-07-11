import json
from calendar_api import CalendarAPI
from constants import TIME_ZONE
from team_scraper import TeamScraper
from unidecode import unidecode

def format_filename(text: str):
    return unidecode(text.lower()).replace(' ', '_')+'.json'

def mount_calendar(summary: str):
    return {
        'summary': summary,
        'timeZone': TIME_ZONE
    }

scraper = TeamScraper()
calendar_api = CalendarAPI()

with open('teams.txt') as file:
    for team_url in file:
        data = scraper.get_info(team_url)
        team = data['team']
        json_filename = format_filename(team)
        calendar = mount_calendar(f'Jogos {team}')
        data['calendar_id'] = calendar_api.create_calendar(calendar)
        
        json_object = json.dumps(data)

        with open(f'./teams/{json_filename}', 'w') as json_file:
            json_file.write(json_object)