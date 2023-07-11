from datetime import datetime
from dataclasses import dataclass

@dataclass
class MatchInfo:
    home: str
    away: str
    datetime: datetime
    competition: str