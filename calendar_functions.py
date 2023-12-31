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
from langchain.agents import Tool, tool


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

@tool
def get_events_on_date(target_date):
    """Used to find events on the calendar for a specific date input is the date"""
    service=create_service()
    target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
    start_time = target_date.isoformat() + 'T00:00:00Z'
    end_time = (target_date + timedelta(days=1)).isoformat() + 'T00:00:00Z'

    # Query events for the specified date
    events_result = service.events().list(
        calendarId='primary', timeMin=start_time, timeMax=end_time).execute()
    events = events_result.get('items', [])

    return events

@tool
def find_event_by_summary(summary):
    """Used to find events on the calendar using the title or summary"""
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

@tool
def create_event(input_str, attendees=None, reminders=None):
    """Used to find events on the calendar needs to have a title,location,description,start_time, and end time as compulsory parameters"""

    item_data = input_str.split(',')
    summary = item_data[0].strip()
    location = item_data[1].strip()
    description = item_data[2].strip()
    start_time = item_data[3].strip()
    end_time=item_data[4].strip()
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
        output =f'{created_event.get("htmlLink")}'
        print(output)
        return output
    except HttpError as e:
        out=f'Error creating event: {e}'
        return json.dumps(output)


def get_events_todays_date(input=None):
    """Used to get todays date"""
    today_date = datetime.now().date()
    today_date=str(today_date)
    events =get_events_on_date(today_date)
    return events



get_events_on_date=Tool(
    name='get_events_on_date',
    func=get_events_on_date,
    description="Used to get the meeting details of a specific date. input is the date in the format 2023-MM-DD"
)

get_events_todays_date = Tool(
    name='get_events_todays_date',
    func=get_events_todays_date,
    description="Use to when you need to get the meetings for today."
)

find_event_by_summary= Tool(
    name='find_event_by_summary',
    func=find_event_by_summary,
    description="Used to find a meeting or event on calendar. input is the meeting name"
)

create_event=Tool(
    name='create_event',
    func=create_event,
    description="Used to create a new event. input is the meeting-name,location, description, start_time as YYYY-MM-DDTHH:MM:SS, end_time in YYYY-MM-DDTHH:MM:SS"
)
tools =[find_event_by_summary,get_events_on_date,get_events_todays_date,create_event]


