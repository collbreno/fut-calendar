from datetime import datetime
from dataclasses import dataclass

@dataclass
class Match:
    id: str
    home: str
    away: str
    datetime: datetime
    competition: str
    flag: str = ''