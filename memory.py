# memory.py
import json
import os

DB_FILE = "users.json"

def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def get_user(user_id):
    users = load_users()
    user_id_str = str(user_id)
    if user_id_str not in users:
        users[user_id_str] = {
            "name": None,
            "username": None,
            "history": [],
            "contact_info": None
        }
        save_users(users)
    return users[user_id_str]

def update_user(user_id, data):
    users = load_users()
    user_id_str = str(user_id)
    if user_id_str not in users:
        users[user_id_str] = {}
    
    users[user_id_str].update(data)
    save_users(users)

def add_message(user_id, role, content):
    users = load_users()
    user_id_str = str(user_id)
    if user_id_str not in users:
        get_user(user_id) # Create if not exists
        users = load_users() # Reload
    
    if "history" not in users[user_id_str]:
        users[user_id_str]["history"] = []
        
    users[user_id_str]["history"].append({"role": role, "content": content})
    # Keep history limited to last 20 messages to save tokens
    if len(users[user_id_str]["history"]) > 20:
        users[user_id_str]["history"] = users[user_id_str]["history"][-20:]
        
    save_users(users)
