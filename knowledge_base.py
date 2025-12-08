# knowledge_base.py
import json
import os

KNOWLEDGE_FILE = "knowledge.json"

def load_knowledge():
    if not os.path.exists(KNOWLEDGE_FILE):
        return {}
    try:
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading knowledge: {e}")
        return {}

def save_knowledge(data):
    with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Load initial data
_data = load_knowledge()

SALES_SCRIPTS = {
    "intro": _data.get("intro", ""),
    "benefits": _data.get("benefits", []),
    "objections": _data.get("objections", {}),
    "closing": _data.get("closing", "")
}

SYSTEM_PROMPT_TEMPLATE = _data.get("system_prompt_template", "")

def reload_knowledge():
    """Reloads the knowledge base from disk (called after admin updates)"""
    global SALES_SCRIPTS, SYSTEM_PROMPT_TEMPLATE, _data
    _data = load_knowledge()
    SALES_SCRIPTS["intro"] = _data.get("intro", "")
    SALES_SCRIPTS["benefits"] = _data.get("benefits", [])
    SALES_SCRIPTS["objections"] = _data.get("objections", {})
    SALES_SCRIPTS["closing"] = _data.get("closing", "")
    SYSTEM_PROMPT_TEMPLATE = _data.get("system_prompt_template", "")
