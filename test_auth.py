from avito_client import AvitoClient
import logging

logging.basicConfig(level=logging.INFO)

def test_auth():
    print("Testing Avito authentication...")
    client = AvitoClient()
    try:
        token = client.get_token()
        print(f"Success! Token received: {token[:10]}...")
        
        user_id = client.get_user_id()
        print(f"User ID: {user_id}")
        
    except Exception as e:
        print(f"Authentication failed: {e}")

if __name__ == "__main__":
    test_auth()
