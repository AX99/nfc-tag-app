import os
from firebase_admin import credentials, initialize_app, firestore


def initialize_firebase(db_id=None):
    """Initializes the Firebase Admin SDK and returns a Firestore client."""
    cred = credentials.Certificate(
        os.path.join(os.path.dirname(__file__), "../../creds/sagc.json")
    )
    initialize_app(credential=cred)
    print("Firebase Admin SDK initialized successfully!")
    return firestore.client(database_id=db_id)
