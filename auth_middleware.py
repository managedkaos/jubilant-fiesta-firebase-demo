from fastapi import Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from firebase_config import FirebaseAuth
from typing import Optional
import json

def get_current_user(request: Request) -> Optional[dict]:
    """Get current user from session or token"""
    # Check for user in session first
    user = request.session.get('user')
    if user:
        return user

    # Check for Firebase token in headers
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        user_info = FirebaseAuth.verify_token(token)
        if user_info:
            # Store user in session
            request.session['user'] = user_info
            return user_info

    return None

def require_auth(request: Request):
    """Dependency to require authentication"""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

def optional_auth(request: Request):
    """Dependency for optional authentication"""
    return get_current_user(request)
