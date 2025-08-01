from flask import Flask, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth
import os

# --------------------------
# 建立 Flask App
# --------------------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")

# --------------------------
# 設定 Google OAuth
# --------------------------
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params={'prompt': 'consent', 'access_type': 'offline'},
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    client_kwargs={'scope': 'openid email profile'},
)

# --------------------------
# 首頁
# --------------------------
@app.route('/')
def index():
    user = session.get('user')
    if user:
        return f"""
        <h2>👋 歡迎 {user['email']}</h2>
        <p>你的 Google 名稱：{user['name']}</p>
        <a href='/logout'>登出</a>
        """
    return '<a href="/login">使用 Google 登入</a>'

# --------------------------
# 登入
# --------------------------
@app.route('/login')
def login():
    redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI")
    return google.authorize_redirect(redirect_uri)

# --------------------------
# OAuth 回調
# --------------------------
@app.route('/auth')
def auth():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session['user'] = user_info
    return redirect('/')

# --------------------------
# 登出
# --------------------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# --------------------------
# 主程式入口
# --------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
