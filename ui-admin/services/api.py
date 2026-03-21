import time
import requests


def call_api(slug, flag, options):
    time.sleep(1)
    response = requests.get("https://a.espncdn.com/i/leaguelogos/soccer/500/4.png")
    return {
        "text": f"Calendar created! https://calendar.google.com/calendario",
        "image_url": response.url
    }