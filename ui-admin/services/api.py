import time
import requests

import time
from datetime import datetime


def toggle_competition(slug, enable: bool):
    import time
    time.sleep(1)  # simulate API call

    # In real case, call your backend here
    return {"success": True}

def get_competitions():
    time.sleep(1.5)  # simulate delay

    return [
        {
            "slug": "eng.1",
            "flag": "",
            "calendar_id": "cal_123",
            "image_url": "https://a.espncdn.com/i/leaguelogos/soccer/500/23.png",
            "name": "Premier League",
            "last_update": datetime.now(),
            "teams": ["Arsenal", "Chelsea", "Liverpool"],
            "use_mapper": True,
            "disabled": False,
        },
        {
            "slug": "esp.1",
            "flag": "",
            "calendar_id": None,
            "image_url": "https://a.espncdn.com/i/leaguelogos/soccer/500/15.png",
            "name": "La Liga",
            "last_update": datetime.now(),
            "teams": ["Real Madrid", "Barcelona"],
            "use_mapper": False,
            "disabled": False,
        },
        {
            "slug": "bra.1",
            "flag": "",
            "calendar_id": "cal_999",
            "image_url": "https://a.espncdn.com/i/leaguelogos/soccer/500/85.png",
            "name": "Campeonato Brasileiro",
            "last_update": datetime.now(),
            "teams": ["Fluminense", "Flamengo"],
            "use_mapper": False,
            "disabled": False,
        },
        {
            "slug": "fifa.world",
            "flag": "",
            "calendar_id": "cal_999",
            "image_url": "https://a.espncdn.com/i/leaguelogos/soccer/500/4.png",
            "name": "Copa do mundo",
            "last_update": datetime.now(),
            "teams": [],
            "use_mapper": False,
            "disabled": True,
        },
    ]

def call_api(slug, flag, options):
    time.sleep(1)
    response = requests.get("https://a.espncdn.com/i/leaguelogos/soccer/500/4.png")
    return {
        "text": f"Calendar created! https://calendar.google.com/calendario",
        "image_url": response.url
    }