import json

j = dict()
with open('schedule.json') as f:
    j = json.load(f)

ids = set()
for event in j['events']:
    if event['season']['slug'] == 'group-stage':
        competition = event['competitions'][0]
        teams = competition['competitors']
        home = teams[0]['team']
        away = teams[1]['team']
        homeId, homeName = home['id'], home['displayName']
        awayId, awayName = away['id'], away['displayName']
        if homeId not in ids:
            print(homeId, homeName)
            ids.add(homeId)
        if awayId not in ids:
            print(awayId, awayName)
            ids.add(awayId)