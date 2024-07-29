from notification.notification import Notification
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class SmsToNotification(Notification):
    def __init__(self):
        self.api_key = os.getenv('SMS_API_KEY')
        self.api_url = 'https://api.sms.to/sms/send'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

    def notify(self, message):
        data = {
            "message": message,
            "to": os.getenv('SMS_TO_NUMBER'),
            "sender_id": os.getenv('SMS_SENDER_ID'),
            "bypass_optout": True,

        }

        response = requests.post(self.api_url, headers=self.headers, json=data)
        print(response.json())
