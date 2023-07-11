from calendar_api import CalendarAPI
from match_to_event import MatchToEvent
from scraper import Scraper
import json

file = open('./settings.json')
data = json.load(file)
team = data['team']
matches_url = data['matches_url']
calendar_id = data['calendar_id']

scraper = Scraper(team=team, url=matches_url)
calendar = CalendarAPI(calendar_id=calendar_id)
conversor = MatchToEvent()

for match in scraper.get_scheduled_matches():
    calendar.upsert(conversor.convert(match))
