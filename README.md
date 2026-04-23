# 🔐 Private 2FA Code Generator

A lightweight, self-hosted web app that generates Time-Based One-Time Passwords (TOTP). Think of it as your own private version of Google Authenticator or Authy that runs directly in your browser.

## Why Use This?

Sometimes you don't want to use your phone for 2FA, or you need to generate codes programmatically for testing. Maybe you just prefer keeping everything on your own machine. This tool lets you:

- **Generate codes instantly** using your secret key.
- **Auto-refresh** every 30 seconds (just like authenticator apps).
- **Accept flexible secrets** (paste with or without spaces).
- **Run locally** so your secrets never leave your computer.

## 🚀 Quick Setup

1. **Clone or download** this folder.
git clone https://github.com/Hitesh9p/2fac.git  
2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install dependencies**
   ```bash
     pip install -r requirements.txt
3. **Install dependencies**
  ```bash
     python 2fa.py
   ```
4. **Open your browser and go to**
  ```bash
     http://localhost:8000
  ```
📖 How to Use
1. Copy your Base32 Secret Key from the service you're setting up (e.g., GitHub, AWS, Discord).
2. Paste it into the input box on the web page.
  ✅ Works with: U4KYLC3X76YOFF6L
  ✅ Works with: U4KY LC3X 76YO FF6L
3. Click Generate Code.
4. The 6-digit code will appear and auto-refresh every 30 seconds.
⚠️ Security Note
This tool is designed for local use.
  Do not expose this publicly on the open internet without adding authentication (like a password or API key).
  Never share your secret key with anyone.
  If you stop using this, clear your browser history/cache to remove any stored secrets.
API Usage
Prefer to call it from a script? The backend exposes a simple endpoint:
  ```bash
curl -X POST http://localhost:8000/code \
  -H "Content-Type: application/json" \
  -d '{"secret": "YOUR_SECRET_HERE"}'
