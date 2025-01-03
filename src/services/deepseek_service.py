from typing import Dict, List
import requests
from ..config import Config
from ...utils.retry import retry_with_backoff

class DeepSeekService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1"  # Replace with actual endpoint
        
    def summarize_email(self, content: str) -> str:
        prompt = f"""
        Summarize the following email content concisely:
        
        {content}
        
        Provide a brief summary focusing on key points and any action items.
        """
        
        response = self._call_api(prompt)
        return response['summary']
    
    def categorize_email(self, subject: str, content: str) -> Dict[str, float]:
        prompt = f"""
        Analyze this email and categorize it based on the following categories:
        {Config.EMAIL_CATEGORIES}
        
        Subject: {subject}
        Content: {content}
        
        Provide category and confidence score.
        """
        
        response = self._call_api(prompt)
        return response['category']
    
    def suggest_action(self, summary: str, category: str) -> Dict:
        prompt = f"""
        Based on this email:
        Summary: {summary}
        Category: {category}
        
        Suggest appropriate actions:
        1. Does it require a response?
        2. Should it be scheduled?
        3. Priority level (1-5)
        """
        
        response = self._call_api(prompt)
        return {
            'needs_response': response['needs_response'],
            'needs_scheduling': response['needs_scheduling'],
            'priority': response['priority']
        }
    
    @retry_with_backoff(retries=3)
    def _call_api(self, prompt: str) -> Dict:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'prompt': prompt,
            'max_tokens': 500
        }
        
        response = requests.post(
            f"{self.base_url}/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"API call failed: {response.text}")
            
        return response.json() 