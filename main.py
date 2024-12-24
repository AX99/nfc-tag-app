import firebase_admin
from firebase_admin import credentials, firestore
import os
from src.config import FIREBASE_DB_ID  # If you decide to keep DB_ID in config

from src.manage_tag import register_tag, fetch_tag


# Initialize Firebase Admin *once*
cred = credentials.Certificate(
    os.path.join(os.path.dirname(__file__), "creds/sagc.json")
)  # Path relative to main.py
firebase_admin.initialize_app(cred)

db = firestore.client(database_id=FIREBASE_DB_ID)


# Example usage
# register_tag("UUID12345", "John Doe", "john.doe@example.com", "+1234567890", db=db)
fetch_tag("UUID12345", db=db)