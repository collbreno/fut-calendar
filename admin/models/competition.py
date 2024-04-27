from dataclasses import dataclass

@dataclass
class Competition:
    id: str
    name: str
    teams: list[str]