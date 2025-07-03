from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'your_calendar_id_here@group.calendar.google.com'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

def get_available_slots(date_str, duration_minutes):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    start = date.replace(hour=9, minute=0)
    end = date.replace(hour=17, minute=0)
    events = service.events().list(calendarId=CALENDAR_ID, timeMin=start.isoformat() + 'Z',
                                   timeMax=end.isoformat() + 'Z', singleEvents=True,
                                   orderBy='startTime').execute().get('items', [])
    busy = [(datetime.fromisoformat(e['start']['dateTime']), datetime.fromisoformat(e['end']['dateTime'])) for e in events]

    free = []
    current = start
    while current + timedelta(minutes=duration_minutes) <= end:
        if all(not (b[0] < current + timedelta(minutes=duration_minutes) and b[1] > current) for b in busy):
            free.append((current, current + timedelta(minutes=duration_minutes)))
        current += timedelta(minutes=30)
    return free

def book_event(start_time, end_time, summary, description):
    event = {
        'summary': summary,
        'description': description,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
    }
    event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return event.get('htmlLink')