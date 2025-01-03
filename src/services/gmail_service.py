from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
from ...utils.retry import retry_with_backoff
import base64
import email

class GmailService:
    def __init__(self, credentials):
        self.service = build('gmail', 'v1', credentials=credentials)
    
    @retry_with_backoff(retries=3)
    def fetch_unread_emails(self, max_results=50):
        try:
            results = self.service.users().messages().list(
                userId='me',
                labelIds=['UNREAD'],
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            return [self._get_email_data(msg['id']) for msg in messages]
        except Exception as e:
            raise Exception(f"Error fetching emails: {str(e)}")
    
    def _get_email_data(self, message_id):
        message = self.service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()
        
        headers = message['payload']['headers']
        subject = next(h['value'] for h in headers if h['name'] == 'Subject')
        sender = next(h['value'] for h in headers if h['name'] == 'From')
        
        return {
            'message_id': message_id,
            'sender': sender,
            'subject': subject,
            'received_date': datetime.fromtimestamp(int(message['internalDate'])/1000),
            'raw_content': self._get_email_content(message)
        }
    
    def _get_email_content(self, message):
        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    return base64.urlsafe_b64decode(
                        part['body']['data']
                    ).decode('utf-8')
        return "" 