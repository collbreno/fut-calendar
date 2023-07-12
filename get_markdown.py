import json
import os

if __name__ == '__main__':
    folder_path = "teams/"

    files = os.listdir(folder_path)

    for filename in files:
        fullpath = os.path.join(folder_path, filename)
        if os.path.isfile(fullpath):
            file = open(fullpath)
            data = json.load(file)
            team = data['team']
            share_url = 'https://calendar.google.com/calendar/u/0/r?cid='+data['calendar_id']
            print(f'[{team}]({share_url})')
