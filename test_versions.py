import requests
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("AVITO_CLIENT_ID")
CLIENT_SECRET = os.getenv("AVITO_CLIENT_SECRET")
CHAT_ID = "u2i-qot2XKHd8o4bd4L4PQAKkg" # From user logs

def get_token():
    url = "https://api.avito.ru/token/"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()['access_token']

def test_versions():
    token = get_token()
    user_id = requests.get("https://api.avito.ru/core/v1/accounts/self", 
                          headers={'Authorization': f'Bearer {token}'}).json()['id']
    print(f"User ID: {user_id}")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    versions = ['v1', 'v2', 'v3']
    
    for v in versions:
        print(f"\nTesting Messenger API {v}...")
        url = f"https://api.avito.ru/messenger/{v}/accounts/{user_id}/chats/{CHAT_ID}/messages"
        try:
            resp = requests.get(url, headers=headers, params={'limit': 1})
            print(f"Status: {resp.status_code}")
            print(f"Response: {resp.text[:200]}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_versions()
