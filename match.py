from datetime import datetime
from dataclasses import dataclass

@dataclass
class MatchInfo:
    team: str
    datetime: datetime
    competition: str
    opponent: str
    isHome: bool