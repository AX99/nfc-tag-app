#!/usr/bin/env python3
"""
NFC Tag Manager - Admin Tool

This script allows you to manage authorized NFC tags in your system.
It connects directly to your Firebase database to:
- Register new authorized tags
- List existing authorized tags
- Check tag status

Run this locally whenever you need to prepare new tags for distribution.
"""

import os
import sys
import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# Add the project root to the path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Import configuration from centralized config
from src.config import FIREBASE_DB_ID, FIREBASE_SERVICE_ACCOUNT_PATH
from src.firebase_manager import FirebaseManager


def initialize_firebase():
    """Initialize Firebase with credentials from centralized config."""
    try:
        # Check if already initialized
        firebase_admin.get_app()
        return firestore.client(database_id=FIREBASE_DB_ID)
    except ValueError:
        # Not initialized, so initialize
        try:
            # Use service account path from config
            cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_PATH)
            firebase_admin.initialize_app(cred)
            return firestore.client(database_id=FIREBASE_DB_ID)
        except (ValueError, FileNotFoundError) as e:
            print(f"Error initializing Firebase: {e}")
            print(
                f"Make sure your service account file exists at: {FIREBASE_SERVICE_ACCOUNT_PATH}"
            )
            sys.exit(1)


def register_tag(manager):
    """Register a new authorized tag."""
    print("\n=== Register New Authorized Tag ===")

    # Get the UUID from user input
    uuid = input("Enter the tag UUID (scan the physical tag): ").strip()

    if not uuid:
        print("UUID cannot be empty.")
        return

    # Check if tag already exists
    if manager.is_authorized_tag(uuid):
        print(f"Tag {uuid} is already registered as an authorized tag.")
        return

    # Register the tag
    try:
        manager.register_authorized_tag(uuid)
        print(f"✅ Tag {uuid} successfully registered as an authorized tag!")
    except (ValueError, ConnectionError) as e:
        print(f"❌ Error registering tag: {e}")


def list_tags(manager):
    """List all authorized tags in the system."""
    print("\n=== Authorized Tags ===")

    try:
        # Get all documents from the authorized_tags collection
        db = manager.db
        tags = db.collection("authorized_tags").stream()

        # Convert to a list so we can check if it's empty
        tag_list = list(tags)

        if not tag_list:
            print("No authorized tags registered yet.")
            return

        # Print the tags
        print(f"{'UUID':<36} | {'Status':<10} | {'Created At':<20}")
        print("-" * 70)

        for tag in tag_list:
            tag_data = tag.to_dict()
            status = "Registered" if tag_data.get("registered") else "Unregistered"
            created_at = tag_data.get("created_at", "Unknown")

            # Format the timestamp if it exists
            if isinstance(created_at, datetime.datetime):
                created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")

            print(f"{tag.id:<36} | {status:<10} | {created_at:<20}")

        print(f"\nTotal: {len(tag_list)} authorized tags")

    except (ConnectionError, ValueError, firebase_admin.exceptions.FirebaseError) as e:
        print(f"❌ Error listing tags: {e}")


def batch_register(manager):
    """Register multiple tags at once from a file."""
    print("\n=== Batch Register Authorized Tags ===")

    file_path = input(
        "Enter the path to the file containing UUIDs (one per line): "
    ).strip()

    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            uuids = [line.strip() for line in f if line.strip()]

        if not uuids:
            print("No UUIDs found in the file.")
            return

        print(f"Found {len(uuids)} UUIDs in the file.")
        confirm = input(f"Register all {len(uuids)} tags? (y/n): ").lower()

        if confirm != "y":
            print("Batch registration cancelled.")
            return

        success_count = 0
        already_exists_count = 0

        for uuid in uuids:
            if manager.is_authorized_tag(uuid):
                print(f"Tag {uuid} is already registered as an authorized tag.")
                already_exists_count += 1
                continue

            manager.register_authorized_tag(uuid)
            success_count += 1
            print(f"✅ Tag {uuid} registered as an authorized tag.")

        print("\nBatch registration complete:")
        print(f"- {success_count} tags successfully registered")
        print(f"- {already_exists_count} tags already existed")

    except (IOError, ValueError, firebase_admin.exceptions.FirebaseError) as e:
        print(f"❌ Error during batch registration: {e}")


def main():
    """Main function to run the admin tool."""
    # Initialize Firebase and create a manager
    db = initialize_firebase()
    manager = FirebaseManager(db)

    print("NFC Tag Manager - Admin Tool")
    print("============================")

    while True:
        print("\nOptions:")
        print("1. Register a new authorized tag")
        print("2. List all authorized tags")
        print("3. Batch register tags from file")
        print("4. Exit")

        choice = input("\nSelect an option (1-4): ").strip()

        if choice == "1":
            register_tag(manager)
        elif choice == "2":
            list_tags(manager)
        elif choice == "3":
            batch_register(manager)
        elif choice == "4":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
