import firebase_admin
from firebase_admin import firestore
import datetime


def register_tag(
    uuid: str, owner_name: str, owner_email: str, owner_phone: str, db=None
):
    """Registers a tag in Firestore.

    Args:
        uuid: The UUID of the tag.
        owner_name: The owner's name.
        owner_email: The owner's email.
        owner_phone: The owner's phone number.
        db:  (Optional) A Firestore client instance.  If not provided, creates a new one.

    Raises:
       ValueError: If the Firebase app hasn't been initialized.
    """
    if db is None:
        try:
            db = firestore.client()
        except ValueError as e:
            raise ValueError(
                "The default Firebase app has not been initialized. "
                "You must either initialize it or pass a db instance explicitly."
            ) from e
    try:
        data = {
            "owner_name": owner_name,
            "owner_email": owner_email,
            "owner_phone": owner_phone,
            "created_at": datetime.datetime.now(datetime.UTC),
        }
        doc_ref = db.collection("tags").document(uuid)

        if doc_ref.get().exists:
            print(f"Tag {uuid} already exists!")
            return

        doc_ref.set(data)
        print(f"Tag {uuid} for {owner_name} registered successfully!")
    except Exception as e:
        print(f"Error registering tag: {e}")


def fetch_tag(uuid: str, db=None):
    """Fetches a tag from Firestore.

    Args:
        uuid: The UUID of the tag.
        db:  (Optional) A Firestore client instance.  If not provided, creates a new one.

    Raises:
       ValueError: If the Firebase app hasn't been initialized.
    """
    if db is None:
        try:
            db = firestore.client()
        except ValueError as e:
            raise ValueError(
                "The default Firebase app has not been initialized. "
                "You must either initialize it or pass a db instance explicitly."
            ) from e
    try:
        tag_ref = db.collection("tags").document(uuid)
        tag = tag_ref.get()
        if tag.exists:
            print(f"Tag {uuid} fetched successfully!")
            print(f"Data: {tag.to_dict()}")
            return tag.to_dict()
        else:
            print(f"No tag found with UUID: {uuid}")
            return None
    except Exception as e:
        print(f"Error fetching tag: {e}")
        return None
