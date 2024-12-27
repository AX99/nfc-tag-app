import datetime
from src.firebase_init.firebase_init import initialize_firebase


class FirebaseManager:
    def __init__(self, db=None):
        """Initialize FirebaseManager with a Firestore client."""
        if db is None:
            self.db = initialize_firebase()  # Use the shared initialization logic
        else:
            self.db = db

    def register_document(self, collection: str, document_id: str, data: dict):
        """Registers a document in the specified Firestore collection."""
        try:
            doc_ref = self.db.collection(collection).document(document_id)
            if doc_ref.get().exists:
                print(f"Document with ID {document_id} already exists in {collection}!")
                return
            doc_ref.set(data)
            print(f"Document {document_id} registered successfully in {collection}!")
        except Exception as e:
            print(f"Error registering document: {e}")
            raise

    def fetch_document(self, collection: str, document_id: str):
        """Fetches a document from the specified Firestore collection."""
        try:
            doc_ref = self.db.collection(collection).document(document_id)
            doc = doc_ref.get()
            if doc.exists:
                print(f"Document {document_id} fetched successfully from {collection}!")
                return doc.to_dict()
            else:
                print(f"No document found with ID: {document_id} in {collection}")
                return None
        except Exception as e:
            print(f"Error fetching document: {e}")
            return None


# Convenience functions for tags and owners
def register_tag(uuid, owner_name, owner_email, owner_phone, db=None):
    """Registers a tag in Firestore.

    Args:
        uuid: The UUID of the tag.
        owner_name: The owner's name.
        owner_email: The owner's email.
        owner_phone: The owner' s phone number.
        db:  (Optional) A Firestore client instance.  If not provided, creates a new one.

    """
    manager = FirebaseManager(db)
    data = {
        "owner_name": owner_name,
        "owner_email": owner_email,
        "owner_phone": owner_phone,
        "created_at": datetime.datetime.now(datetime.UTC),
    }
    manager.register_document("tags", uuid, data)


def fetch_tag(uuid, db=None):
    manager = FirebaseManager(db)
    return manager.fetch_document("tags", uuid)


# def register_owner(uuid, owner_name, owner_email, owner_phone, db=None):
#     manager = FirebaseManager(db)
#     data = {
#         "owner_name": owner_name,
#         "owner_email": owner_email,
#         "owner_phone": owner_phone,
#         "created_at": datetime.datetime.now(datetime.UTC),
#     }
#     manager.register_document("owners", uuid, data)
