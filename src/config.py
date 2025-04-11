import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Firebase Configuration
FIREBASE_DB_ID = os.environ.get("FIREBASE_DB_ID", "nfc-tag-store")
FIREBASE_SERVICE_ACCOUNT_PATH = os.environ.get(
    "FIREBASE_SERVICE_ACCOUNT_PATH", "creds/sagc.json"
)
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS", "creds/sagc.json"
)

# Application Settings
DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "t", "1")
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

# Email Configuration (for future notification features)
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
NOTIFICATION_EMAIL = os.environ.get("NOTIFICATION_EMAIL", "")