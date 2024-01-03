import json
import os

def print_all():
    folder_path = "teams/"

    files = os.listdir(folder_path)

    for filename in files:
        fullpath = os.path.join(folder_path, filename)
        if os.path.isfile(fullpath):
            file = open(fullpath)
            data = json.load(file)
            team = data['team']
            flag = data.get('flag', '')
            if flag != '':
                team += f' {flag}'
            share_url = 'https://calendar.google.com/calendar/u/0/r?cid='+data['calendar_id']
            print(f'[{team}]({share_url})\n')
