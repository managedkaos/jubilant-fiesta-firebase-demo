# 🔥 Firebase Auth Demo with FastAPI

A comprehensive web application demonstrating Firebase authentication, FastAPI backend, and Firestore data persistence. This project showcases modern web development practices with secure authentication and user data management.

## ✨ Features

- **🔓 Public Pages**: Accessible to all users
- **🔐 Firebase Authentication**: Secure login/signup with Firebase Auth
- **🛡️ Private Pages**: Protected routes requiring authentication
- **💾 User Data Persistence**: Store and retrieve user data with Cloud Firestore
- **👤 User Profiles**: Personalized user experience with customizable preferences
- **📊 Dashboard**: User statistics and account information
- **🚪 Session Management**: Secure logout functionality

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   Firebase      │
│   (HTML/JS)     │◄──►│   Backend       │◄──►│   Services      │
│                 │    │                 │    │                 │
│ • Public Pages  │    │ • Auth Routes   │    │ • Authentication│
│ • Login Forms   │    │ • Private Pages │    │ • Firestore DB  │
│ • Dashboard     │    │ • API Endpoints │    │ • User Data     │
│ • Profile       │    │ • Session Mgmt  │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Firebase project
- pip (Python package manager)

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd jubilant-fiesta-firebase-demo

# Run the setup script
python setup.py
```

### 2. Firebase Configuration

1. **Create a Firebase Project**:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create a new project or select existing one

2. **Enable Authentication**:
   - Go to Authentication → Sign-in method
   - Enable Email/Password authentication

3. **Enable Firestore Database**:
   - Go to Firestore Database
   - Create database in test mode

4. **Get Firebase Config**:
   - Go to Project Settings → General
   - Scroll to "Your apps" section
   - Click web app icon (</>)
   - Copy the `firebaseConfig` object

5. **Create Service Account**:
   - Go to Project Settings → Service accounts
   - Click "Generate new private key"
   - Save as `firebase-service-account.json` in project root

6. **Update Configuration**:
   - Edit `.env` file with your Firebase settings
   - Update `FIREBASE_CONFIG` in `main.py`

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python main.py
```

The application will be available at `http://localhost:8000`

## 📁 Project Structure

```
jubilant-fiesta-firebase-demo/
├── main.py                      # Main FastAPI application
├── firebase_config.py           # Firebase configuration and utilities
├── auth_middleware.py           # Authentication middleware
├── config.py                    # Application configuration
├── setup.py                     # Setup script
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (created by setup)
├── static/                      # Static files directory
├── firebase-service-account.json # Firebase service account (you provide)
└── README.md                    # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Firebase Configuration
FIREBASE_API_KEY=your-api-key
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=123456789
FIREBASE_APP_ID=your-app-id

# Application Configuration
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True
```

## 🛣️ API Endpoints

### Public Endpoints

- `GET /` - Public homepage with login/signup forms
- `GET /static/*` - Static files

### Authentication Endpoints

- `POST /auth/login` - User login
- `POST /auth/signup` - User registration
- `POST /auth/logout` - User logout

### Protected Endpoints

- `GET /dashboard` - User dashboard (requires auth)
- `GET /profile` - User profile page (requires auth)
- `POST /api/update-profile` - Update user profile (requires auth)
- `POST /api/update-preferences` - Update user preferences (requires auth)

## 🔐 Security Features

- **Firebase Authentication**: Industry-standard authentication
- **Session Management**: Secure session handling
- **Token Verification**: Server-side token validation
- **Protected Routes**: Authentication-required endpoints
- **Environment Variables**: Secure configuration management

## 🎨 User Interface

The application features a modern, responsive design with:

- **Gradient Backgrounds**: Beautiful visual appeal
- **Card-based Layout**: Clean, organized content
- **Responsive Design**: Works on all device sizes
- **Interactive Elements**: Smooth user experience
- **Status Indicators**: Clear feedback for user actions

## 📊 Data Model

### User Document Structure (Firestore)

```json
{
  "uid": "user-unique-id",
  "email": "user@example.com",
  "name": "Display Name",
  "created_at": "timestamp",
  "last_login": "timestamp",
  "updated_at": "timestamp",
  "preferences": {
    "theme": "light|dark",
    "notifications": true|false
  }
}
```

## 🧪 Testing

To test the application:

1. **Public Access**: Visit `/` without logging in
2. **Registration**: Create a new account
3. **Login**: Sign in with existing credentials
4. **Dashboard**: Access private dashboard
5. **Profile**: Update user information
6. **Logout**: Sign out and verify session clearing

## 🚨 Troubleshooting

### Common Issues

1. **Firebase Connection Error**:
   - Verify service account JSON file exists
   - Check Firebase project configuration
   - Ensure Firestore is enabled

2. **Authentication Failures**:
   - Verify Firebase Auth is enabled
   - Check API keys in configuration
   - Ensure email/password auth is enabled

3. **Import Errors**:
   - Run `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

4. **Port Already in Use**:
   - Change port in `main.py` or kill existing process
   - Use `lsof -ti:8000 | xargs kill` to free port

### Debug Mode

Enable debug mode by setting `DEBUG=True` in `.env` file for detailed error messages.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Firebase](https://firebase.google.com/) - Authentication and database
- [Firestore](https://firebase.google.com/docs/firestore) - NoSQL database

## 📞 Support

For questions or issues:

1. Check the troubleshooting section
2. Review Firebase documentation
3. Open an issue on GitHub

---

**Happy Coding! 🚀**
