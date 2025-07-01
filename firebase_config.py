import firebase_admin
from firebase_admin import credentials, auth, firestore
import os
from typing import Optional

# Initialize Firebase Admin SDK
# You'll need to download your Firebase service account key and place it in the project
# or set the GOOGLE_APPLICATION_CREDENTIALS environment variable
try:
    # Try to initialize with service account file
    if os.path.exists('firebase-service-account.json'):
        cred = credentials.Certificate('firebase-service-account.json')
        firebase_admin.initialize_app(cred)
    else:
        # Try to initialize with default credentials (for development)
        firebase_admin.initialize_app()
except Exception as e:
    print(f"Firebase initialization error: {e}")
    print("Please ensure you have proper Firebase credentials set up")

# Initialize Firestore
db = firestore.client()

class FirebaseAuth:
    @staticmethod
    def verify_token(id_token: str) -> Optional[dict]:
        """Verify Firebase ID token and return user info"""
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            print(f"Token verification error: {e}")
            return None

    @staticmethod
    def get_user_by_uid(uid: str) -> Optional[dict]:
        """Get user data from Firestore"""
        try:
            user_doc = db.collection('users').document(uid).get()
            if user_doc.exists:
                return user_doc.to_dict()
            return None
        except Exception as e:
            print(f"Error getting user data: {e}")
            return None

    @staticmethod
    def create_or_update_user(uid: str, user_data: dict):
        """Create or update user data in Firestore"""
        try:
            db.collection('users').document(uid).set(user_data, merge=True)
            return True
        except Exception as e:
            print(f"Error creating/updating user: {e}")
            return False
