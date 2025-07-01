#!/usr/bin/env python3
"""
Test script to verify Firebase configuration
"""

from config import Config
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Get Firebase configuration
firebase_config = Config.get_firebase_config()

print("Firebase Configuration:")
print(json.dumps(firebase_config, indent=2))

print("\nChecking for None values:")
for key, value in firebase_config.items():
    if value is None:
        print(f"❌ {key}: None")
    else:
        print(f"✅ {key}: {value}")

print(f"\nSecret Key: {Config.SECRET_KEY}")
print(f"Debug Mode: {Config.DEBUG}")
