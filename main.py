from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
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

# Get Firebase configuration
FIREBASE_CONFIG = Config.get_firebase_config()

# 1. Public Page
@app.get("/", response_class=HTMLResponse)
async def public_page(request: Request):
    user = get_current_user(request)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Firebase Auth Demo - Public Page</title>
        <script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-app-compat.js"></script>
        <script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-auth-compat.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .nav {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
            .btn {{ padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin: 5px; }}
            .btn-primary {{ background: #007bff; color: white; }}
            .btn-success {{ background: #28a745; color: white; }}
            .btn-danger {{ background: #dc3545; color: white; }}
            .welcome {{ background: #e7f3ff; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .auth-section {{ text-align: center; margin: 20px 0; }}
            #loginForm, #signupForm {{ display: none; margin: 20px 0; }}
            .form-group {{ margin: 10px 0; }}
            input {{ padding: 10px; border: 1px solid #ddd; border-radius: 5px; width: 100%; max-width: 300px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔥 Firebase Auth Demo</h1>
                <p>A simple web application demonstrating Firebase authentication with FastAPI</p>
            </div>

            <div class="nav">
                <div>
                    <a href="/" class="btn btn-primary">Public Page</a>
                    <a href="/dashboard" class="btn btn-success">Dashboard</a>
                    <a href="/profile" class="btn btn-success">Profile</a>
                </div>
                <div>
                    {f'<span>Welcome, {user["email"] if user else "Guest"}!</span>' if user else '<span>Not logged in</span>'}
                </div>
            </div>

            {f'''
            <div class="welcome">
                <h3>Welcome, {user.get('email', 'User')}!</h3>
                <p>You are logged in and can access private pages.</p>
                <button onclick="logout()" class="btn btn-danger">Logout</button>
            </div>
            ''' if user else '''
            <div class="auth-section">
                <h3>Welcome to our Demo App!</h3>
                <p>This is a publicly accessible page. Please log in to access private features.</p>
                <button onclick="showLoginForm()" class="btn btn-primary">Login</button>
                <button onclick="showSignupForm()" class="btn btn-success">Sign Up</button>

                <div id="loginForm">
                    <h4>Login</h4>
                    <div class="form-group">
                        <input type="email" id="loginEmail" placeholder="Email" required>
                    </div>
                    <div class="form-group">
                        <input type="password" id="loginPassword" placeholder="Password" required>
                    </div>
                    <button onclick="login()" class="btn btn-primary">Login</button>
                </div>

                <div id="signupForm">
                    <h4>Sign Up</h4>
                    <div class="form-group">
                        <input type="email" id="signupEmail" placeholder="Email" required>
                    </div>
                    <div class="form-group">
                        <input type="password" id="signupPassword" placeholder="Password" required>
                    </div>
                    <button onclick="signup()" class="btn btn-success">Sign Up</button>
                </div>
            </div>
            '''}

            <div style="margin-top: 30px;">
                <h3>Features Demo</h3>
                <ul>
                    <li>✅ Public page (this page)</li>
                    <li>✅ Firebase authentication</li>
                    <li>✅ Private pages (Dashboard & Profile)</li>
                    <li>✅ User data persistence with Firestore</li>
                    <li>✅ Session management</li>
                </ul>
            </div>
        </div>

        <script>
            // Firebase configuration
            const firebaseConfig = {json.dumps(FIREBASE_CONFIG)};
            firebase.initializeApp(firebaseConfig);

            function showLoginForm() {{
                document.getElementById('loginForm').style.display = 'block';
                document.getElementById('signupForm').style.display = 'none';
            }}

            function showSignupForm() {{
                document.getElementById('signupForm').style.display = 'block';
                document.getElementById('loginForm').style.display = 'none';
            }}

            async function login() {{
                const email = document.getElementById('loginEmail').value;
                const password = document.getElementById('loginPassword').value;

                try {{
                    const userCredential = await firebase.auth().signInWithEmailAndPassword(email, password);
                    const idToken = await userCredential.user.getIdToken();

                    // Send token to backend
                    const response = await fetch('/auth/login', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${{idToken}}`
                        }}
                    }});

                    if (response.ok) {{
                        window.location.reload();
                    }} else {{
                        alert('Login failed');
                    }}
                }} catch (error) {{
                    alert('Login error: ' + error.message);
                }}
            }}

            async function signup() {{
                const email = document.getElementById('signupEmail').value;
                const password = document.getElementById('signupPassword').value;

                try {{
                    const userCredential = await firebase.auth().createUserWithEmailAndPassword(email, password);
                    const idToken = await userCredential.user.getIdToken();

                    // Send token to backend
                    const response = await fetch('/auth/signup', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${{idToken}}`
                        }}
                    }});

                    if (response.ok) {{
                        window.location.reload();
                    }} else {{
                        alert('Signup failed');
                    }}
                }} catch (error) {{
                    alert('Signup error: ' + error.message);
                }}
            }}

            async function logout() {{
                try {{
                    await firebase.auth().signOut();
                    const response = await fetch('/auth/logout', {{ method: 'POST' }});
                    if (response.ok) {{
                        window.location.reload();
                    }}
                }} catch (error) {{
                    alert('Logout error: ' + error.message);
                }}
            }}
        </script>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)

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

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard - Private Page</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
            .nav {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
            .btn {{ padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin: 5px; }}
            .btn-primary {{ background: #007bff; color: white; }}
            .btn-danger {{ background: #dc3545; color: white; }}
            .dashboard-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
            .stat-card {{ background: white; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="nav">
                <div>
                    <a href="/" class="btn btn-primary">Public Page</a>
                    <a href="/dashboard" class="btn btn-primary">Dashboard</a>
                    <a href="/profile" class="btn btn-primary">Profile</a>
                </div>
                <div>
                    <span>Welcome, {user.get('email', 'User')}!</span>
                    <button onclick="logout()" class="btn btn-danger">Logout</button>
                </div>
            </div>

            <h1>📊 Dashboard</h1>
            <p>This is a private page - only visible when logged in!</p>

            <div class="dashboard-card">
                <h3>Your Account Information</h3>
                <p><strong>Email:</strong> {user.get('email', 'N/A')}</p>
                <p><strong>User ID:</strong> {user.get('uid', 'N/A')}</p>
                <p><strong>Last Login:</strong> {user_data.get('last_login', 'N/A') if user_data else 'N/A'}</p>
            </div>

            <div class="stats">
                <div class="stat-card">
                    <h3>🎯 Total Logins</h3>
                    <p style="font-size: 2em; color: #007bff;">{user_data.get('login_count', 1) if user_data else 1}</p>
                </div>
                <div class="stat-card">
                    <h3>📅 Member Since</h3>
                    <p style="font-size: 1.2em; color: #28a745;">{user_data.get('created_at', 'Today') if user_data else 'Today'}</p>
                </div>
                <div class="stat-card">
                    <h3>⚙️ Preferences</h3>
                    <p style="font-size: 1.2em; color: #ffc107;">{len(user_data.get('preferences', {})) if user_data else 0} settings</p>
                </div>
            </div>

            <div class="dashboard-card">
                <h3>Quick Actions</h3>
                <button onclick="window.location.href='/profile'" class="btn btn-primary">Edit Profile</button>
                <button onclick="updatePreferences()" class="btn btn-primary">Update Preferences</button>
            </div>
        </div>

        <script>
            async function logout() {{
                const response = await fetch('/auth/logout', {{ method: 'POST' }});
                if (response.ok) {{
                    window.location.href = '/';
                }}
            }}

            async function updatePreferences() {{
                const response = await fetch('/api/update-preferences', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        theme: 'dark',
                        notifications: false
                    }})
                }});

                if (response.ok) {{
                    alert('Preferences updated!');
                    window.location.reload();
                }}
            }}
        </script>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)

@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/")

    # Get user data from Firestore
    user_data = FirebaseAuth.get_user_by_uid(user['uid'])

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Profile - Private Page</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
            .nav {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
            .btn {{ padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin: 5px; }}
            .btn-primary {{ background: #007bff; color: white; }}
            .btn-danger {{ background: #dc3545; color: white; }}
            .profile-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .form-group {{ margin: 15px 0; }}
            label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
            input, textarea {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
            .preferences {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="nav">
                <div>
                    <a href="/" class="btn btn-primary">Public Page</a>
                    <a href="/dashboard" class="btn btn-primary">Dashboard</a>
                    <a href="/profile" class="btn btn-primary">Profile</a>
                </div>
                <div>
                    <span>Welcome, {user.get('email', 'User')}!</span>
                    <button onclick="logout()" class="btn btn-danger">Logout</button>
                </div>
            </div>

            <h1>👤 Profile</h1>
            <p>Manage your account settings and preferences</p>

            <div class="profile-card">
                <h3>Personal Information</h3>
                <div class="form-group">
                    <label for="name">Display Name</label>
                    <input type="text" id="name" value="{user_data.get('name', '') if user_data else ''}" placeholder="Enter your name">
                </div>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" value="{user.get('email', '')}" readonly>
                </div>
                <button onclick="updateProfile()" class="btn btn-primary">Update Profile</button>
            </div>

            <div class="profile-card">
                <h3>Preferences</h3>
                <div class="preferences">
                    <div>
                        <label>
                            <input type="checkbox" id="notifications" {'checked' if user_data and user_data.get('preferences', {}).get('notifications', True) else ''}>
                            Enable Notifications
                        </label>
                    </div>
                    <div>
                        <label for="theme">Theme</label>
                        <select id="theme">
                            <option value="light" {'selected' if user_data and user_data.get('preferences', {}).get('theme') == 'light' else ''}>Light</option>
                            <option value="dark" {'selected' if user_data and user_data.get('preferences', {}).get('theme') == 'dark' else ''}>Dark</option>
                        </select>
                    </div>
                </div>
                <button onclick="updatePreferences()" class="btn btn-primary">Save Preferences</button>
            </div>

            <div class="profile-card">
                <h3>Account Statistics</h3>
                <p><strong>User ID:</strong> {user.get('uid', 'N/A')}</p>
                <p><strong>Created:</strong> {user_data.get('created_at', 'N/A') if user_data else 'N/A'}</p>
                <p><strong>Last Login:</strong> {user_data.get('last_login', 'N/A') if user_data else 'N/A'}</p>
            </div>
        </div>

        <script>
            async function logout() {{
                const response = await fetch('/auth/logout', {{ method: 'POST' }});
                if (response.ok) {{
                    window.location.href = '/';
                }}
            }}

            async function updateProfile() {{
                const name = document.getElementById('name').value;
                const response = await fetch('/api/update-profile', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ name: name }})
                }});

                if (response.ok) {{
                    alert('Profile updated successfully!');
                }} else {{
                    alert('Failed to update profile');
                }}
            }}

            async function updatePreferences() {{
                const notifications = document.getElementById('notifications').checked;
                const theme = document.getElementById('theme').value;

                const response = await fetch('/api/update-preferences', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        notifications: notifications,
                        theme: theme
                    }})
                }});

                if (response.ok) {{
                    alert('Preferences updated successfully!');
                }} else {{
                    alert('Failed to update preferences');
                }}
            }}
        </script>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)

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
