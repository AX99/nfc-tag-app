import os
from firebase_admin import credentials, initialize_app, firestore
from src.config import FIREBASE_DB_ID, FIREBASE_SERVICE_ACCOUNT_PATH


def initialize_firebase(db_id=None):
    """Initializes the Firebase Admin SDK and returns a Firestore client.

    Uses configuration from src.config for credentials and database ID.
    """
    # Use provided db_id or fall back to config
    if db_id is None:
        db_id = FIREBASE_DB_ID

    # Initialize Firebase with credentials from config
    cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_PATH)
    initialize_app(credential=cred)
    print("Firebase Admin SDK initialized successfully!")

    # Return Firestore client with database ID
    return firestore.client(database_id=db_id)
