import requests
import time
import logging
from config import AVITO_CLIENT_ID, AVITO_CLIENT_SECRET

logger = logging.getLogger(__name__)

class AvitoClient:
    def __init__(self):
        self.client_id = AVITO_CLIENT_ID
        self.client_secret = AVITO_CLIENT_SECRET
        self.base_url = "https://api.avito.ru"
        self.token = None
        self.token_expires_at = 0

    def get_token(self):
        if self.token and time.time() < self.token_expires_at:
            return self.token
        
        url = "https://api.avito.ru/token/"
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            data = response.json()
            self.token = data['access_token']
            self.token_expires_at = time.time() + data['expires_in'] - 60 # buffer
            logger.info("Successfully obtained Avito access token")
            return self.token
        except Exception as e:
            logger.error(f"Failed to get token: {e}")
            raise

    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.get_token()}',
            'Content-Type': 'application/json'
        }

    def get_chats(self, limit=100):
        """Get list of chats"""
        url = f"{self.base_url}/messenger/v2/accounts/{self.get_user_id()}/chats"
        params = {'limit': limit}
        response = requests.get(url, headers=self.get_headers(), params=params)
        response.raise_for_status()
        return response.json().get('chats', [])

    def get_messages(self, chat_id, limit=50):
        url = f"{self.base_url}/messenger/v3/accounts/{self.get_user_id()}/chats/{chat_id}/messages"
        params = {'limit': limit}
        response = requests.get(url, headers=self.get_headers(), params=params)
        response.raise_for_status()
        return response.json().get('messages', [])

    def send_message(self, chat_id, text):
        url = f"{self.base_url}/messenger/v1/accounts/{self.get_user_id()}/chats/{chat_id}/messages"
        payload = {
            'message': {
                'text': text
            },
            'type': 'text'
        }
        response = requests.post(url, headers=self.get_headers(), json=payload)
        response.raise_for_status()
        return response.json()

    def get_user_id(self):
        """
        We need the user_id (profile_id) for messenger API. 
        We can get it from the User Info API or maybe it's the client_id? 
        Actually, for messenger API we usually need the user_id associated with the token.
        Let's fetch it from /core/v1/accounts/self if available, 
        or assume we can find it via /messenger/v1/accounts (but that requires ID).
        
        Avito API documentation says 'user_id' in path.
        Use /core/v1/accounts/self to identify the current user.
        """
        # Simple cache for user_id to avoid repeated calls
        if hasattr(self, '_user_id') and self._user_id:
            return self._user_id

        url = f"{self.base_url}/core/v1/accounts/self"
        response = requests.get(url, headers=self.get_headers())
        response.raise_for_status()
        self._user_id = response.json().get('id')
        return self._user_id
