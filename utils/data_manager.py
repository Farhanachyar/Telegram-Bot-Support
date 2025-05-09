import json
from config import TRACKING_FILE, CONVERSATIONS_FILE
from helper import logger

def load_tracking_data():
    """Load message tracking data from file"""
    try:
        with open(TRACKING_FILE, "r") as f:
            data = json.load(f)
            logger.info(f"Loaded {len(data)} tracked users from file")
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        logger.info("No existing tracking file found or file is corrupted. Creating new tracking")
        return {}

def load_conversations_data():
    """Load conversations data from file"""
    try:
        with open(CONVERSATIONS_FILE, "r") as f:
            data = json.load(f)
            logger.info(f"Loaded conversations for {len(data)} users")
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        logger.info("No existing conversations file found or file is corrupted. Creating new")
        return {}

def save_tracking_data(data):
    """Save message tracking data to file"""
    with open(TRACKING_FILE, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"Saved tracking data for {len(data)} users")

def save_conversations_data(data):
    """Save conversations data to file"""
    with open(CONVERSATIONS_FILE, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"Saved conversations for {len(data)} users")