from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Shoutboxx Calendar'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    event = {
    'summary': 'Test Event',
    'location': 'BITS Pilani, Hyderabad Campus',
    'description': 'Insert random stuff here',
    'start': {
        'dateTime': '2017-01-04T01:35:00+05:30',
        'timeZone': 'Asia/Kolkata',
    },
    'end': {
        'dateTime': '2017-01-04T02:35:00+05:30',
        'timeZone': 'Asia/Kolkata',
    },
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 1},
        {'method': 'popup', 'minutes': 1},
      ],
    },
  }

    event = service.events().insert(calendarId='primary', body=event).execute()

if __name__ == '__main__':
    main()