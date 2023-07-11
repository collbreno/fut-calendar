from calendar_api import CalendarAPI
from match_to_event import MatchToEvent
from scraper import Scraper

scraper = Scraper(team='Fluminense', url='https://br.soccerway.com/teams/brazil/fluminense-football-club/312/matches/')
calendar = CalendarAPI(calendar_id='primary')
conversor = MatchToEvent()

for match in scraper.get_scheduled_matches():
    calendar.create(conversor.convert(match))
