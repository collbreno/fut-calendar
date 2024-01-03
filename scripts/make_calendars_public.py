import json
import os

from services.calendar_api import CalendarAPI

def make_all_public():
    folder_path = "teams/"

    files = os.listdir(folder_path)
    calendar_api = CalendarAPI()

    for filename in files:
        fullpath = os.path.join(folder_path, filename)
        if os.path.isfile(fullpath):
            file = open(fullpath)
            data = json.load(file)
            calendar_api.make_public(data['calendar_id'])
