import time
import requests
from sqlalchemy.exc import SQLAlchemyError
from app.db.models import ETLError
from dotenv import load_dotenv
import os

load_dotenv(encoding='utf-8')

top_stories_url = os.getenv("TOP_STORIES_URL")
item_url = os.getenv("ITEM_URL")

def fetch_top_story_ids(session, max_retries=5, backoff_factor=1):
    for attempt in range(max_retries):
        try:
            response = requests.get(top_stories_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            wait = backoff_factor * (2 ** attempt)
            error_msg = f"[topstories] Attempt {attempt + 1} failed: {e}. Retrying in {wait}s..."
            print(error_msg)
            log_error(session, None, error_msg)
            time.sleep(wait)

    return []


def fetch_story_details(session, story_id, max_retries=5, backoff_factor=1):
    for attempt in range(max_retries):
        try:
            response = requests.get(item_url.format(story_id), timeout=10)
            response.raise_for_status()
            data = response.json()
            if data and data.get("type") == "story":
                return {
                    "id": data["id"],
                    "title": data.get("title", "No Title"),
                    "score": data.get("score", None),
                    "url": data.get("url"),
                    "author": data.get("by", "Unknown"),
                    "time": data.get("time", None),
                    "descendants": data.get("descendants"),
                    "type": data.get("type")
                }
        except Exception as e:
            wait = backoff_factor * (2 ** attempt)
            error_msg = f"[story {story_id}] Attempt {attempt + 1} failed: {e}. Retrying in {wait}s..."
            print(error_msg)
            log_error(session, story_id, error_msg)
            time.sleep(wait)

    return None


def log_error(session, story_id, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            error = ETLError(
                story_id=story_id,
                error_message=str(message)
            )
            session.add(error)
            session.commit()
            print(f"Logged error for story {story_id} successfully.")
            return
        except SQLAlchemyError as e:
            session.rollback()  # Rollback in case of error to clear the session state
            print(f"Error logging failed for story {story_id}: {e}. Retrying ({attempt + 1}/{max_retries})...")
        time.sleep(1)  # Optional: delay before retrying
    print(f"Failed to log error for story {story_id} after {max_retries} attempts.")
