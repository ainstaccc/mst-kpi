from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "test_secret")

# Google OAuth 設定
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    client_kwargs={
        'scope': 'openid email profile',
        'redirect_uri': os.environ.get("OAUTH_REDIRECT_URI", "https://你的render網址/login/callback")
    }
)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/login/google')
def login_google():
    return google.authorize_redirect(url_for('auth_callback', _external=True))

@app.route('/login/callback')
def auth_callback():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    # 這裡可以檢查 email 是否符合你公司 Gmail 名單
    session['user'] = user_info
    return f"登入成功！歡迎 {user_info['email']}"
