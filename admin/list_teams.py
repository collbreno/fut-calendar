import json
import sys
import requests

if len(sys.argv) < 2:
    raise Exception('Competition slug not provided')

slug = sys.argv[1]

url = f'https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/teams'
response = requests.get(url).json()
league = response['sports'][0]['leagues'][0]

for team in league['teams']:
    team = team['team']
    team_id = team['id']
    team_name = team['name']
    print(team_id, team_name)
