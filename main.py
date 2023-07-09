from scraper import Scraper

scraper = Scraper()

for match in scraper.get_scheduled_matches():
    print(match)
