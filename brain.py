# brain.py
import os
from openai import OpenAI
from dotenv import load_dotenv
from knowledge_base import SYSTEM_PROMPT_TEMPLATE, SALES_SCRIPTS
from memory import get_user, add_message

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_response(user_id, user_message, username=None):
    # Reload knowledge to ensure we have the latest edits from Admin Panel
    import knowledge_base
    knowledge_base.reload_knowledge()

    # 1. Retrieve user context
    user_data = get_user(user_id)
    
    # Update username if provided and different
    if username and user_data.get("username") != username:
        from memory import update_user
        update_user(user_id, {"username": username})
        user_data["username"] = username

    user_name = user_data.get("name") or "Неизвестный"
    history = user_data.get("history", [])

    # 2. Add user message to memory
    add_message(user_id, "user", user_message)

    # 3. Construct System Prompt
    # Format history for the prompt (last 5 messages for context in prompt text if needed, 
    # but we will send full history to API)
    history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history[-10:]])
    
    system_prompt = knowledge_base.SYSTEM_PROMPT_TEMPLATE.format(
        user_name=user_name,
        history=history_text
    )

    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    # Add conversation history to the API call
    for msg in history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # Add the current user message explicitly since 'history' was fetched before update
    messages.append({"role": "user", "content": user_message})

    print(f"DEBUG: Sending messages to OpenAI: {messages}")


    print(f"DEBUG: Sending messages to OpenAI: {messages}")


    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Or gpt-3.5-turbo if 4o not available, but 4o is better for sales
            messages=messages,
            temperature=0.7
        )
        
        ai_message = response.choices[0].message.content
        
        # Check for ACTION: SAVE_CONTACT
        if "ACTION: SAVE_CONTACT" in ai_message:
            try:
                # Extract the line
                lines = ai_message.split('\n')
                new_lines = []
                for line in lines:
                    if line.strip().startswith("ACTION: SAVE_CONTACT"):
                        # Parse Name and Phone
                        import re
                        name_match = re.search(r'Name="([^"]+)"', line)
                        phone_match = re.search(r'Phone="([^"]+)"', line)
                        
                        updates = {}
                        if name_match and name_match.group(1) != "None":
                            updates["name"] = name_match.group(1)
                        if phone_match and phone_match.group(1) != "None":
                            updates["contact_info"] = phone_match.group(1)
                            
                        if updates:
                            from memory import update_user
                            update_user(user_id, updates)
                            print(f"DEBUG: Updated user {user_id} with {updates}")
                    else:
                        new_lines.append(line)
                
                ai_message = "\n".join(new_lines).strip()
            except Exception as e:
                print(f"Error parsing contact action: {e}")

        # 4. Save AI response to memory
        add_message(user_id, "assistant", ai_message)


        return ai_message

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error generating response: {e}")
        return "Извините, я задумался. Можете повторить?"
