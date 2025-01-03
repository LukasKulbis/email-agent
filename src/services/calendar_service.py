from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

class CalendarService:
    def __init__(self, credentials):
        self.service = build('calendar', 'v3', credentials=credentials)
    
    def create_event(self, summary: str, description: str, start_time: datetime, 
                    duration_minutes: int = 60) -> dict:
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
        }
        
        try:
            event = self.service.events().insert(
                calendarId='primary',
                body=event
            ).execute()
            return event
        except Exception as e:
            raise Exception(f"Failed to create calendar event: {str(e)}") 