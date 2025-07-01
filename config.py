import os
from dotenv import load_dotenv
load_dotenv()
from typing import Dict, Any

class Config:
    """Application configuration"""

    # Firebase Configuration
    # Replace these with your actual Firebase project settings
    FIREBASE_CONFIG = {
        "apiKey": os.getenv("FIREBASE_API_KEY", None),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", None),
        "projectId": os.getenv("FIREBASE_PROJECT_ID", None),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", None),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", None),
        "appId": os.getenv("FIREBASE_APP_ID", None),
        "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID", None)
    }

    # Session Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", None)
    SESSION_MAX_AGE = 3600  # 1 hour

    # App Configuration
    APP_TITLE = "Firebase Auth Demo"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Database Configuration
    FIRESTORE_COLLECTION_USERS = "users"

    @classmethod
    def get_firebase_config(cls) -> Dict[str, Any]:
        """Get Firebase configuration"""
        return cls.FIREBASE_CONFIG.copy()

    @classmethod
    def get_session_config(cls) -> Dict[str, Any]:
        """Get session configuration"""
        return {
            "secret_key": cls.SECRET_KEY,
            "max_age": cls.SESSION_MAX_AGE
        }
