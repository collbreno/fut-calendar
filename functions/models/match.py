from datetime import datetime
from dataclasses import dataclass

@dataclass
class Match:
    home: str
    away: str
    datetime: datetime
    competition: str
    flag: str = ''