from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


class CalendarAPI:
    def __init__(self) -> None:
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())


    def __insert(self, calendar_id, event):
        try:
            service = build('calendar', 'v3', credentials=self.creds)
            result = service.events().insert(calendarId=calendar_id, body=event).execute()
            print('Event created', result.get('summary'))

        except HttpError as error:
            print('An error occurred: %s' % error)
    
    def upsert(self, calendar_id, event):
        try:
            service = build('calendar', 'v3', credentials=self.creds)
            result = service.events().update(eventId=event['id'], calendarId=calendar_id, body=event).execute()
            print('Event updated', result.get('summary'))

        except HttpError as error:
            if error.status_code == 404:
                self.__insert(calendar_id, event)
            else:
                print('An error occurred: %s' % error)

    def create_calendar(self, calendar):
        try:
            service = build('calendar', 'v3', credentials=self.creds)
            result = service.calendars().insert(body=calendar).execute()
            print('Calendar created', result.get('summary'))
            return result.get('id')

        except HttpError as error:
            print('An error occurred: %s' % error)