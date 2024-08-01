from notification.notification import Notification
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class PushoverNotification(Notification):
    def __init__(self):
        self.api_url = 'https://api.pushover.net/1/messages.json'

    def notify(self, message):
        data = {
            "message": message,
            "user": os.getenv('PUSHOVER_USER_KEY'),
            "token": os.getenv('PUSHOVER_API_KEY'),

        }

        response = requests.post(self.api_url, json=data)
        print(response.json())

