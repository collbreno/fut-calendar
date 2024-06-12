class TeamsMapper:
    def __init__(self, map_flag: dict[str, str], map_langs: list[dict]) -> None:
        self.map_flag = map_flag
        self.map_langs = map_langs

    def get_team(self, team_id: str) -> str:
        return self.map_flag[team_id]
    
    def get_description(self, home_id: str, away_id: str, competition: str) -> str:
        l = []
        for map_lang in self.map_langs:
            l.append(f'{map_lang[home_id]} x {map_lang[away_id]}')
        l.append(competition)
        return '\n'.join(l)
        