import datetime
import os.path
from datetime import timedelta
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/calendar"]

def create_service():
    creds = None
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
    service = build("calendar", "v3", credentials=creds)
    return service


def get_events_on_date(target_date):
    service=create_service()
    start_time = target_date.isoformat() + 'T00:00:00Z'
    end_time = (target_date + timedelta(days=1)).isoformat() + 'T00:00:00Z'

    # Query events for the specified date
    events_result = service.events().list(
        calendarId='primary', timeMin=start_time, timeMax=end_time).execute()
    events = events_result.get('items', [])

    return events

def find_event_by_summary(summary):
    service=create_service()
    events_result = service.events().list(
        calendarId='primary', q=summary).execute()
    events = events_result.get('items', [])

    if not events:
        print(f'No events found with summary "{summary}"')
        return None

    for event in events:
        print(f'Summary: {event["summary"]}')
        print(f'Start Time: {event["start"].get("dateTime", event["start"].get("date"))}')
        print(f'End Time: {event["end"].get("dateTime", event["end"].get("date"))}')
        print(f'Location: {event.get("location", "N/A")}')
        print('---')

    return events


def create_event(summary, location, description, start_time, end_time, attendees=None, reminders=None):
    service=create_service()
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'UTC',  # Adjust timezone as needed
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'UTC',
        },
        'attendees': attendees,
        'reminders': reminders,
    }

    try:
        created_event = service.events().insert(
            calendarId='primary', body=event).execute()
        output =f'Event created: {created_event.get("htmlLink")}'
        print(output)
        return json.dumps(output)
    except HttpError as e:
        print(f'Error creating event: {e}')