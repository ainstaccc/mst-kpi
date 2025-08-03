import os
import json
import traceback
from flask import Flask, request, redirect, session, send_from_directory
import requests

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = os.environ.get("FLASK_SECRET", "dev_secret_key")

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")

# Google OAuth 2.0 URL
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

@app.route('/')
def index():
    # 首頁顯示 index.html
    try:
        return send_from_directory('static', 'index.html')
    except Exception as e:
        print("首頁載入錯誤：", e, flush=True)
        return "首頁載入錯誤，請查看 Render Logs"

@app.route('/login')
def login():
    # 進入 Google OAuth
    try:
        state = "secure_random_state"
        scope = "openid email profile"
        auth_url = (
            f"{GOOGLE_AUTH_URL}?response_type=code"
            f"&client_id={GOOGLE_CLIENT_ID}"
            f"&redirect_uri={GOOGLE_REDIRECT_URI}"
            f"&scope={scope}"
            f"&state={state}"
            f"&access_type=offline"
        )
        return redirect(auth_url)
    except Exception as e:
        print("登入導向錯誤：", e, flush=True)
        print(traceback.format_exc(), flush=True)
        return "登入導向錯誤，請查看 Render Logs"

@app.route('/login/callback')
def login_callback():
    try:
        code = request.args.get("code")
        if not code:
            return "授權失敗，未取得 code", 400

        # 交換 Token
        token_data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        token_resp = requests.post(GOOGLE_TOKEN_URL, data=token_data)
        token_json = token_resp.json()
        print("Token Response:", token_json, flush=True)

        # 使用 access_token 取得使用者資料
        access_token = token_json.get("access_token")
        if not access_token:
            return "無法取得 Access Token", 400

        userinfo_resp = requests.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        userinfo = userinfo_resp.json()
        print("User Info:", userinfo, flush=True)

        # 簡單回傳使用者資料測試
        return f"登入成功！<br>使用者資訊：<pre>{json.dumps(userinfo, indent=2)}</pre>"

    except Exception as e:
        print("登入 Callback 錯誤：", e, flush=True)
        print(traceback.format_exc(), flush=True)
        return "伺服器錯誤，請查看 Render Logs"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
