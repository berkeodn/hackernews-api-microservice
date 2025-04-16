from fastapi import Header, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")  # Use environment variable for security

def api_key_auth(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")
