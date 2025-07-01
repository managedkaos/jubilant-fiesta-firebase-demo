#!/usr/bin/env python3
"""
Setup script for Firebase Auth Demo
This script helps you configure your Firebase project and install dependencies.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def create_env_file():
    """Create a .env file with Firebase configuration"""
    env_content = """# Firebase Configuration
# Replace these values with your actual Firebase project settings
FIREBASE_API_KEY=your-api-key
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=123456789
FIREBASE_APP_ID=your-app-id

# Application Configuration
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True
"""

    env_file = Path(".env")
    if env_file.exists():
        print("⚠️  .env file already exists. Skipping creation.")
        return

    with open(env_file, "w") as f:
        f.write(env_content)
    print("✅ Created .env file with Firebase configuration template")

def create_firebase_service_account_instructions():
    """Print instructions for setting up Firebase service account"""
    print("\n" + "="*60)
    print("🔥 FIREBASE SETUP INSTRUCTIONS")
    print("="*60)
    print("""
To complete the Firebase setup, you need to:

1. Go to the Firebase Console (https://console.firebase.google.com/)
2. Create a new project or select an existing one
3. Enable Authentication:
   - Go to Authentication > Sign-in method
   - Enable Email/Password authentication
4. Enable Firestore Database:
   - Go to Firestore Database
   - Create database in test mode
5. Get your Firebase config:
   - Go to Project Settings > General
   - Scroll down to "Your apps" section
   - Click on the web app (</>) icon
   - Copy the firebaseConfig object
6. Create a service account key:
   - Go to Project Settings > Service accounts
   - Click "Generate new private key"
   - Save the JSON file as 'firebase-service-account.json' in this directory
7. Update the .env file with your Firebase configuration
8. Update the FIREBASE_CONFIG in main.py with your actual values

For more detailed instructions, visit:
https://firebase.google.com/docs/web/setup
""")

def main():
    """Main setup function"""
    print("🚀 Setting up Firebase Auth Demo...")

    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install dependencies. Please check your Python environment.")
        sys.exit(1)

    # Create .env file
    create_env_file()

    # Create static directory
    static_dir = Path("static")
    static_dir.mkdir(exist_ok=True)
    print("✅ Created static directory")

    # Print Firebase setup instructions
    create_firebase_service_account_instructions()

    print("\n" + "="*60)
    print("🎉 Setup completed!")
    print("="*60)
    print("""
Next steps:
1. Configure your Firebase project (see instructions above)
2. Update the .env file with your Firebase settings
3. Run the application: python main.py
4. Open http://localhost:8000 in your browser

Happy coding! 🚀
""")

if __name__ == "__main__":
    main()
