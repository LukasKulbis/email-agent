from prefect import flow, task
from ..services.gmail_service import GmailService
from ..services.deepseek_service import DeepSeekService
from ..services.calendar_service import CalendarService
from ..database.models import Email
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

@task
def fetch_new_emails(gmail_service: GmailService):
    return gmail_service.fetch_unread_emails()

@task
def process_email(email_data: dict, deepseek_service: DeepSeekService):
    summary = deepseek_service.summarize_email(email_data['raw_content'])
    category = deepseek_service.categorize_email(
        email_data['subject'], 
        email_data['raw_content']
    )
    
    action_suggestions = deepseek_service.suggest_action(summary, category)
    
    return {
        **email_data,
        'summary': summary,
        'category': category,
        'action_suggestions': action_suggestions
    }

@task
def take_actions(processed_email: dict, 
                 calendar_service: CalendarService,
                 gmail_service: GmailService):
    actions_taken = []
    
    if processed_email['action_suggestions']['needs_scheduling']:
        # Create calendar event
        event = calendar_service.create_event(
            summary=f"Follow-up: {processed_email['subject']}",
            description=processed_email['summary'],
            start_time=datetime.now() + timedelta(days=1)  # Schedule for tomorrow
        )
        actions_taken.append(f"Created calendar event: {event['id']}")
    
    return actions_taken

@task
def save_to_database(processed_email: dict, actions_taken: list, session: Session):
    email = Email(
        message_id=processed_email['message_id'],
        sender=processed_email['sender'],
        subject=processed_email['subject'],
        received_date=processed_email['received_date'],
        summary=processed_email['summary'],
        category=processed_email['category'],
        is_processed=True,
        action_taken=', '.join(actions_taken),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    session.add(email)
    session.commit()

@flow(name="Email Processing Flow")
def process_emails():
    try:
        # Initialize services
        gmail_service = GmailService(credentials)  # Add credentials
        deepseek_service = DeepSeekService(Config.DEEPSEEK_API_KEY)
        calendar_service = CalendarService(credentials)  # Add credentials
        
        # Fetch new emails
        new_emails = fetch_new_emails(gmail_service)
        
        for email_data in new_emails:
            # Process each email
            processed_email = process_email(email_data, deepseek_service)
            
            # Take appropriate actions
            actions_taken = take_actions(
                processed_email,
                calendar_service,
                gmail_service
            )
            
            # Save to database
            save_to_database(processed_email, actions_taken, session)  # Add session
            
    except Exception as e:
        logging.error(f"Error in email processing flow: {str(e)}")
        raise 