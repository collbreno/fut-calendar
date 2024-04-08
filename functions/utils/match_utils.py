from unidecode import unidecode
from models.match import Match
import re

class MatchUtils:
    @staticmethod
    def generateID(match: Match):
        pattern = r'[^a-v0-9]'
        id = ''
        for arg in [match.home, match.away, match.competition, match.datetime.year]:
            r = str(arg)
            r = r.lower()
            r = unidecode(r)
            r = re.sub(pattern, '', r)
            id += r
        return id
    


