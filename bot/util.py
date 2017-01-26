import argparse
import datetime
from httplib2 import Http
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from constants import Google


try:
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES = Google.SCOOPES
CLIENT_SECRET_FILE = '../client_secret.json'
APPLICATION_NAME = Google.APPLICATION_NAME


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
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_event():
    credentials = get_credentials()
    http = credentials.authorize(Http())
    service = discovery.build('calendar', 'v3', http=http)
    tomorrow = datetime.datetime.utcnow().today().strftime('%Y-%m-%d') + 'T23:59:59Z'
    now = datetime.datetime.utcnow().today().strftime('%Y-%m-%d') + 'T00:00:00Z'
    event_result = service.events().list(
        calendarId='primary', timeMin=now, timeMax=tomorrow, maxResults=10, singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = event_result.get('items', [])
    result = []
    if not events:
        return None
    for event in events:
        start = datetime.datetime.strptime(
            event['start'].get('dateTime', event['start'].get('date'))[0:-6],
            '%Y-%m-%dT%H:%M:%S'
        ).hour
        result.append((start, event['summary']))
    return result


def get_summarized_entities(entities, min_confidence):
    result = {}
    for entity, values in entities['entities'].iteritems():
        confidence = values[0]['confidence']
        if confidence >= min_confidence:
            result[entity] = values[0]['value']
    return result
