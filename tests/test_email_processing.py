import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from src.services.gmail_service import GmailService
from src.services.deepseek_service import DeepSeekService
from src.services.calendar_service import CalendarService
from src.workflows.email_workflow import process_email, take_actions

@pytest.fixture
def sample_email_data():
    return {
        'message_id': '12345',
        'sender': 'test@example.com',
        'subject': 'Test Email',
        'received_date': datetime.now(),
        'raw_content': 'This is a test email content'
    }

@pytest.fixture
def mock_deepseek_service():
    service = Mock(spec=DeepSeekService)
    service.summarize_email.return_value = "Test summary"
    service.categorize_email.return_value = "AI_CONSULTING"
    service.suggest_action.return_value = {
        'needs_response': True,
        'needs_scheduling': True,
        'priority': 3
    }
    return service

@pytest.fixture
def mock_calendar_service():
    service = Mock(spec=CalendarService)
    service.create_event.return_value = {'id': 'event123'}
    return service

def test_process_email(sample_email_data, mock_deepseek_service):
    result = process_email(sample_email_data, mock_deepseek_service)
    
    assert result['summary'] == "Test summary"
    assert result['category'] == "AI_CONSULTING"
    assert 'action_suggestions' in result
    assert result['action_suggestions']['needs_response'] is True

def test_take_actions(sample_email_data, mock_calendar_service):
    processed_email = {
        **sample_email_data,
        'action_suggestions': {
            'needs_scheduling': True
        }
    }
    
    actions = take_actions(processed_email, mock_calendar_service, None)
    assert len(actions) == 1
    assert 'Created calendar event' in actions[0] 