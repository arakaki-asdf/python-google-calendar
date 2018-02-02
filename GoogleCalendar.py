from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from datetime import date

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class GoogleCalendar:
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Calendar API Python Quickstart'

    def __init__(self):
        pass

    def _get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def getEvents(self, year):
        credentials = self._get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        calendar_id = 'ja.japanese#holiday@group.v.calendar.google.com'
        calendar_min = date(year=year, month=1, day=1).isoformat() + 'T00:00:00.000000Z'
        calendar_max = date(year=year, month=12, day=31).isoformat() + 'T00:00:00.000000Z'

        event_results = service.events().list(
        calendarId = calendar_id,
        timeMin = calendar_min,
        timeMax = calendar_max,
        maxResults = 50,
        singleEvents = True,
        orderBy = "startTime"
        ).execute()

        events = event_results.get('items', [])
        
        return events;
