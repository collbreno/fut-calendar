from calendar_api import CalendarAPI
from match_to_event import MatchToEvent
from scraper import Scraper

scraper = Scraper()
calendar = CalendarAPI()
conversor = MatchToEvent()

for match in scraper.get_scheduled_matches():
    calendar.create(conversor.convert(match))
