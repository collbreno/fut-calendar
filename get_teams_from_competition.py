from competition_scraper import CompetitionScraper

if __name__ == '__main__':
    url = 'https://br.soccerway.com/national/brazil/serie-a/2023/regular-season/r73825/tables/'
    for team in CompetitionScraper().get_teams(url):
        print(team)