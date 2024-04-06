from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class CalendarAPI:
    def __init__(self, creds) -> None:
        self.service = build('calendar', 'v3', credentials=creds)

    def insert(self, calendar_id, event):
        result = self.service.events().insert(calendarId=calendar_id, body=event).execute()
        print('Event created:', result.get('summary'))

    def __update(self, calendar_id, event):
        result = self.service.events().update(eventId=event['id'], calendarId=calendar_id, body=event).execute()
        print('Event updated', result.get('summary'))
    
    def upsert(self, calendar_id, event):
        try:
            self.__update(calendar_id, event)
        except HttpError as error:
            if error.status_code == 404:
                self.insert(calendar_id, event)
            else:
                raise error

    def make_public(self, calendar_id):
        rule = {
            'scope': {
                'type': 'default'
            },
            'role': 'reader'
        }
        self.service.acl().insert(calendarId=calendar_id, body=rule).execute()
        print(f'Calendar {calendar_id} now is public!')
    
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

    def list_acl(self, calendar_id):
        return self.service.acl().list(calendarId=calendar_id).execute()


    def create_calendar(self, calendar):
        try:
            result = self.service.calendars().insert(body=calendar).execute()
            print('Calendar created:', result.get('summary'))
            return result.get('id')

        except HttpError as error:
            print('An error occurred: %s' % error)