from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from auth_middleware import get_current_user, require_auth, optional_auth
from firebase_config import FirebaseAuth
from firebase_admin import firestore
from config import Config
import json
import os
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title=Config.APP_TITLE, version=Config.APP_VERSION)

# Add session middleware
session_config = Config.get_session_config()
app.add_middleware(
    SessionMiddleware,
    secret_key=session_config["secret_key"],
    max_age=session_config["max_age"]
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Get Firebase configuration
FIREBASE_CONFIG = Config.get_firebase_config()
GOOGLE_CLIENT_ID = Config.GOOGLE_CLIENT_ID

# 1. Public Page
@app.get("/", response_class=HTMLResponse)
async def public_page(request: Request):
    user = get_current_user(request)

    return templates.TemplateResponse("public.html", {
        "request": request,
        "user": user,
        "firebase_config": FIREBASE_CONFIG,
        "google_client_id": GOOGLE_CLIENT_ID
    })

# 2. Authentication Endpoints
@app.post("/auth/login")
async def login(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=401, detail="Invalid token")

    token = auth_header.split(' ')[1]
    user_info = FirebaseAuth.verify_token(token)

    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Store user in session
    request.session['user'] = user_info

    # Create or update user in Firestore
    user_data = {
        'email': user_info.get('email'),
        'name': user_info.get('name', ''),
        'last_login': firestore.SERVER_TIMESTAMP,
        'uid': user_info.get('uid')
    }
    FirebaseAuth.create_or_update_user(user_info['uid'], user_data)

    return {"message": "Login successful"}

@app.post("/auth/signup")
async def signup(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=401, detail="Invalid token")

    token = auth_header.split(' ')[1]
    user_info = FirebaseAuth.verify_token(token)

    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Store user in session
    request.session['user'] = user_info

    # Create user in Firestore
    user_data = {
        'email': user_info.get('email'),
        'name': user_info.get('name', ''),
        'created_at': firestore.SERVER_TIMESTAMP,
        'last_login': firestore.SERVER_TIMESTAMP,
        'uid': user_info.get('uid'),
        'preferences': {
            'theme': 'light',
            'notifications': True
        }
    }
    FirebaseAuth.create_or_update_user(user_info['uid'], user_data)

    return {"message": "Signup successful"}

@app.post("/auth/google-login")
async def google_login(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=401, detail="Invalid token")

    token = auth_header.split(' ')[1]
    user_info = FirebaseAuth.verify_token(token)

    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Store user in session
    request.session['user'] = user_info

    # Create or update user in Firestore
    user_data = {
        'email': user_info.get('email'),
        'name': user_info.get('name', user_info.get('display_name', '')),
        'last_login': firestore.SERVER_TIMESTAMP,
        'uid': user_info.get('uid'),
        'auth_provider': 'google',
        'photo_url': user_info.get('picture', ''),
        'email_verified': user_info.get('email_verified', False)
    }

    # Only set created_at if user doesn't exist
    existing_user = FirebaseAuth.get_user_by_uid(user_info['uid'])
    if not existing_user:
        user_data['created_at'] = firestore.SERVER_TIMESTAMP
        user_data['preferences'] = {
            'theme': 'light',
            'notifications': True
        }

    FirebaseAuth.create_or_update_user(user_info['uid'], user_data)

    return {"message": "Google login successful"}

@app.post("/auth/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logout successful"}

# 3. Private Pages
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/")

    # Get user data from Firestore
    user_data = FirebaseAuth.get_user_by_uid(user['uid'])

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "user_data": user_data,
        "firebase_config": FIREBASE_CONFIG
    })

@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/")

    # Get user data from Firestore
    user_data = FirebaseAuth.get_user_by_uid(user['uid'])

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user,
        "user_data": user_data,
        "firebase_config": FIREBASE_CONFIG
    })

# 4. API Endpoints for User Data
@app.post("/api/update-profile")
async def update_profile(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    data = await request.json()
    name = data.get('name', '')

    user_data = {
        'name': name,
        'updated_at': firestore.SERVER_TIMESTAMP
    }

    success = FirebaseAuth.create_or_update_user(user['uid'], user_data)
    if success:
        return {"message": "Profile updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update profile")

@app.post("/api/update-preferences")
async def update_preferences(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    data = await request.json()

    user_data = {
        'preferences': {
            'theme': data.get('theme', 'light'),
            'notifications': data.get('notifications', True)
        },
        'updated_at': firestore.SERVER_TIMESTAMP
    }

    success = FirebaseAuth.create_or_update_user(user['uid'], user_data)
    if success:
        return {"message": "Preferences updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update preferences")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
