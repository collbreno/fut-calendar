from services.calendar_api import CalendarOAuthApi

if __name__ == '__main__':
    calendar_api = CalendarOAuthApi()
    print(type(calendar_api.service))
    # calendars = calendar_api.list_calendars()
    # for calendar in calendars:
    #     calendar_api.delete_acl(calendar['id'])