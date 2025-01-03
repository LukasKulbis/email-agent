from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
from ..config import Config
import logging

logger = logging.getLogger(__name__)

class AuthService:
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/calendar.events'
    ]
    
    def __init__(self):
        self.credentials_path = 'credentials.json'
        self.token_path = 'token.pickle'
    
    def get_credentials(self) -> Credentials:
        """Get and refresh Google API credentials."""
        credentials = None
        
        # Load existing token
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                credentials = pickle.load(token)
        
        # Refresh token if expired
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
                logger.info("Credentials refreshed successfully")
            except Exception as e:
                logger.error(f"Failed to refresh credentials: {str(e)}")
                credentials = None
        
        # If no valid credentials, run authentication flow
        if not credentials:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                credentials = flow.run_local_server(port=0)
                
                # Save credentials
                with open(self.token_path, 'wb') as token:
                    pickle.dump(credentials, token)
                logger.info("New credentials obtained and saved")
            except Exception as e:
                logger.error(f"Authentication flow failed: {str(e)}")
                raise
        
        return credentials 