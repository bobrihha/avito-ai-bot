import time
import logging
import asyncio
from avito_client import AvitoClient
from brain import get_ai_response
from config import OPENAI_API_KEY

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
POLL_INTERVAL = 10  # seconds

class AvitoBot:
    def __init__(self):
        self.client = AvitoClient()
        self.processed_messages = set() # Simple memory to avoid double-replying in this session
        
    def start(self):
        logger.info("Starting Avito Bot...")
        if not OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY is not set. parsing might fail.")

        while True:
            try:
                self.check_new_messages()
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
            
            time.sleep(POLL_INTERVAL)

    def check_new_messages(self):
        logger.info("Checking for new messages...")
        try:
            chats = self.client.get_chats(limit=20)
            for chat in chats:
                chat_id = chat.get('id')
                # Check if text exists in context or somewhere?
                # Avito API 'chats' endpoint usually returns last message info
                last_message = chat.get('last_message')
                if not last_message:
                    continue
                
                # We need to determine if we should reply.
                # Simplest logic: if last message is NOT from us and we haven't processed it.
                # However, 'last_message' structure needs to be checked.
                # Assuming 'author_id' vs 'user_id' check.
                
                # Fetch full messages to be sure (or trust last_message)
                messages = self.client.get_messages(chat_id, limit=1)
                if not messages:
                    continue
                    
                latest_msg = messages[0]
                msg_id = latest_msg.get('id')
                author_id = latest_msg.get('author_id')
                my_id = self.client.get_user_id()
                
                if author_id != my_id and msg_id not in self.processed_messages:
                    # It's a message for us!
                    content = latest_msg.get('content', {}).get('text', '')
                    logger.info(f"New message from chat {chat_id}: {content}")
                    
                    # Generate AI response
                    # Using a placeholder username since Avito might not give it easily
                    response = get_ai_response(user_id=chat_id, user_text=content, username="AvitoUser")
                    
                    # Send response
                    logger.info(f"Sending response: {response}")
                    self.client.send_message(chat_id, response)
                    
                    # Mark as processed
                    self.processed_messages.add(msg_id)
                    
        except Exception as e:
            logger.error(f"Error checking messages: {e}")

if __name__ == "__main__":
    bot = AvitoBot()
    bot.start()
