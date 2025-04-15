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
        except (ValueError, TypeError) as e:
            print(f"Error with document ID or collection: {e}")
            raise
        except ImportError as e:
            print(f"Firebase import error: {e}")
            raise
        except RuntimeError as e:
            print(f"Runtime error fetching document: {e}")
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
        except (ValueError, TypeError) as e:
            print(f"Error with document ID or collection: {e}")
            return None
        except ImportError as e:
            print(f"Firebase import error: {e}")
            return None
        except RuntimeError as e:
            print(f"Runtime error fetching document: {e}")
            return None

    def is_authorized_tag(self, uuid: str):
        """Checks if a tag UUID is authorized (pre-registered in the system).

        Args:
            uuid: The UUID of the tag to check.

        Returns:
            bool: True if the tag is authorized, False otherwise.
        """
        # Check if the UUID exists in the authorized_tags collection
        authorized_tag = self.fetch_document("authorized_tags", uuid)
        return authorized_tag is not None

    def register_authorized_tag(self, uuid: str):
        """Pre-registers a tag as authorized in the system.

        This should be called during your manufacturing/preparation process,
        before distributing tags to users.

        Args:
            uuid: The UUID of the tag to register as authorized.
        """
        data = {
            "created_at": datetime.datetime.now(datetime.UTC),
            "registered": False,  # Will be set to True when a user registers it
        }
        self.register_document("authorized_tags", uuid, data)

    def mark_tag_as_registered(self, uuid: str):
        """Marks an authorized tag as registered by a user.

        Args:
            uuid: The UUID of the tag.
        """
        authorized_tag_ref = self.db.collection("authorized_tags").document(uuid)
        authorized_tag_ref.update({"registered": True})


# Convenience functions for tags and owners
def register_tag(uuid, owner_name, owner_email, owner_phone, manager):
    """Registers a tag in Firestore.

    Args:
        uuid: The UUID of the tag.
        owner_name: The owner's name.
        owner_email: The owner's email.
        owner_phone: The owner's phone number.
        manager: The FirebaseManager instance.

    Returns:
        bool: True if registration was successful, False if the tag is not authorized.
    """
    # First check if this is an authorized tag
    if not manager.is_authorized_tag(uuid):
        print(f"Tag {uuid} is not authorized!")
        return False

    # Create the tag data
    data = {
        "owner_name": owner_name,
        "owner_email": owner_email,
        "owner_phone": owner_phone,
        "created_at": datetime.datetime.now(datetime.UTC),
    }

    # Register the tag
    manager.register_document("registered_tags", uuid, data)

    # Mark the tag as registered in the authorized_tags collection
    manager.mark_tag_as_registered(uuid)

    return True


def fetch_tag(uuid, manager):
    """Fetches a tag from Firestore using its UUID.

    Args:
        uuid: The UUID of the tag.
        manager: The FirebaseManager instance.

    Returns:
        The tag data or None if not found.
    """
    return manager.fetch_document("registered_tags", uuid)
