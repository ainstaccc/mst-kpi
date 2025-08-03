# app.py
# ------------------------
# Flask + Google OAuth2 Web App
# 加入完整錯誤捕捉，方便 Render Logs 除錯
# ------------------------

from flask import Flask, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth
import os
import traceback

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")

# OAuth 設定
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)

@app.route('/')
def index():
    user = session.get('user')
    if user:
        return f"已登入，歡迎 {user.get('email', '未知帳號')}！"
    return '<a href="/login">使用 Google 登入</a>'

@app.route('/login')
def login():
    redirect_uri = url_for('auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/login/callback')
def auth_callback():
    try:
        # 取得 OAuth Token
        token = google.authorize_access_token()
        print("OAuth Token:", token, flush=True)

        if not token:
            return "授權失敗：未取得 Token，請查看 Logs"

        # 嘗試解析使用者資訊
        try:
            user_info = google.parse_id_token(token)
        except Exception as e:
            print("ID Token 解析失敗：", e, flush=True)
            user_info = None

        if not user_info:
            # 改用 API 取得基本資料
            resp = google.get('userinfo')
            user_info = resp.json() if resp else {}

        print("User Info:", user_info, flush=True)
        session['user'] = user_info

        return f"登入成功！歡迎 {user_info.get('email', '未知帳號')}"

    except Exception as e:
        print("登入錯誤：", e, flush=True)
        print(traceback.format_exc(), flush=True)
        return "伺服器錯誤，請查看 Render Logs"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
