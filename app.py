from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

# 建立 Flask App
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "test_secret")

# ======================
# Google OAuth 設定
# ======================
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    client_kwargs={
        'scope': 'openid email profile',
        # 注意：redirect_uri 在 authorize_redirect() 時動態傳入
    }
)

@app.route('/')
def home():
    """首頁，回傳靜態 index.html"""
    return app.send_static_file('index.html')

@app.route('/login/google')
def login_google():
    """Google OAuth 登入"""
    redirect_uri = url_for('auth_callback', _external=True)
    # Debug Log 確認 URI
    print("Google OAuth redirect URI:", redirect_uri, flush=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/login/callback')
def auth_callback():
    """Google OAuth 登入回調"""
    token = google.authorize_access_token()
    print("OAuth Token:", token, flush=True)

    user_info = google.parse_id_token(token)
    print("User Info:", user_info, flush=True)

    # 將使用者資料存進 session
    session['user'] = user_info
    return f"登入成功！歡迎 {user_info.get('email', '未知帳號')}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
