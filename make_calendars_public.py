import json
import os

from calendar_api import CalendarAPI

if __name__ == '__main__':
    folder_path = "teams/"

    files = os.listdir(folder_path)
    calendar_api = CalendarAPI()

    for filename in files:
        fullpath = os.path.join(folder_path, filename)
        if os.path.isfile(fullpath):
            file = open(fullpath)
            data = json.load(file)
            calendar_api.make_public(data['calendar_id'])
