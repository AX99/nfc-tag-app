import os
from firebase_admin import credentials, initialize_app, firestore
from src.config import FIREBASE_DB_ID

def initialize_firebase():
    """Initializes the Firebase Admin SDK and returns a Firestore client."""
    cred = credentials.Certificate(
        os.path.join(os.path.dirname(__file__), "../../creds/sagc.json")
    )
    initialize_app(cred)
    return firestore.client(database_id=FIREBASE_DB_ID)
