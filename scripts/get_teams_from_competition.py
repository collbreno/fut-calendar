from scrapers.competition_scraper import CompetitionScraper

def get_serie_a():
    url = 'https://br.soccerway.com/national/brazil/serie-a/2023/regular-season/r73825/tables/'
    for team in CompetitionScraper().get_teams(url):
        print(team)