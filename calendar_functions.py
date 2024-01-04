import os
from dotenv import load_dotenv
load_dotenv()
conig_file_path = os.getenv("CONFIG_FILE_PATH")

import datetime
import os.path
from datetime import timedelta
from datetime import datetime

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
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials_2.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    service = build("calendar", "v3", credentials=creds)
    return service



def get_events_on_date(target_date: str) -> str:
    service=create_service()
    target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
    start_time = target_date.isoformat() + 'T00:00:00Z'
    end_time = (target_date + timedelta(days=1)).isoformat() + 'T00:00:00Z'

    # Query events for the specified date
    events_result = service.events().list(
        calendarId='primary', timeMin=start_time, timeMax=end_time).execute()
    events = events_result.get('items', [])

    return events


def find_event_by_summary(summary: str) ->str:
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

def create_event(meeting_name: str,description: str, start_time: str, end_time: str, location: str=None,attendees: str=None, reminders: str=None) ->str:
    service=create_service()
    event = {
        'summary': meeting_name,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'UTC+05:30',  # Adjust timezone as needed
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'UTC+05:30',
        },
        'attendees': attendees,
        'reminders': reminders,
    }

    try:
        created_event = service.events().insert(
            calendarId='primary', body=event).execute()
        output =f'{created_event.get("htmlLink")}'
        print(output)
        return output
    except HttpError as e:
        out=f'Error creating event: {e}'
        return json.dumps(output)



def today(n: int) -> str:
    today_date = datetime.now().date()
    return str(today_date)






