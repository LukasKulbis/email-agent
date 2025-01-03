from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # API Credentials
    GMAIL_CREDENTIALS = os.getenv('GMAIL_CREDENTIALS')
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    
    # Database
    DATABASE_URL = "sqlite:///emails.db"
    
    # Email Processing
    MAX_EMAILS_PER_FETCH = 50
    EMAIL_FETCH_INTERVAL = 300  # 5 minutes
    
    # Categories
    EMAIL_CATEGORIES = [
        "AI_CONSULTING",
        "BLOCKCHAIN",
        "MEETING_REQUEST",
        "URGENT",
        "FOLLOW_UP",
        "OTHER"
    ] 