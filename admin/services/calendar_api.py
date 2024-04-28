import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pprint import pprint
from constants import LOCAL_TIME_ZONE

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


class CalendarOAuthApi:
    def __init__(self) -> None:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        self.service = build("calendar", "v3", credentials=creds)

    def list_calendars(self):
        calendars = []
        page_token = None
        while True:
            calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for calendar in calendar_list['items']:
                calendars.append(calendar)
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        return calendars
    
    def list_acl(self, calendar_id):
        acl = self.service.acl().list(calendarId=calendar_id).execute()
        pprint(acl)

    def make_public(self, calendar_id):
        rule = {
            'scope': {
                'type': 'default'
            },
            'role': 'reader'
        }
        self.service.acl().insert(calendarId=calendar_id, body=rule).execute()
        print(f'Calendar {calendar_id} is now public!')
    
    def add_as_writer(self, calendar_id, email):
        rule = {
            'scope': {
                'type': 'user',
                'value': email,
            },
            'role': 'writer'
        }
        self.service.acl().insert(calendarId=calendar_id, body=rule).execute()
        print(f'User {email} is now writer of {calendar_id}!')

    def create_calendar(self, summary):
        calendar = {
            'summary': summary,
            'timeZone': LOCAL_TIME_ZONE
        }
        result = self.service.calendars().insert(body=calendar).execute()
        return result['id']

