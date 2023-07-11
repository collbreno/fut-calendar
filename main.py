from calendar_api import CalendarAPI
from match_to_event import MatchToEvent
from matches_scraper import MatchesScraper
import json

file = open('./settings.json')
data = json.load(file)
matches_url = data['matches_url']
calendar_id = data['calendar_id']

matches_scraper = MatchesScraper(url=matches_url)
calendar = CalendarAPI()
conversor = MatchToEvent()

for match in matches_scraper.get_scheduled_matches():
    calendar.upsert(calendar_id, conversor.convert(match))
