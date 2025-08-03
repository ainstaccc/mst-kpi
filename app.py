from flask import Flask, render_template, redirect, request, session, url_for
import os
import requests

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_secret")

# Google OAuth 環境變數
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "https://mst-kpi.onrender.com/callback")
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

@app.route("/")
def index():
    return render_template("index.html")  # 使用原本的首頁

@app.route("/login")
def login():
    auth_url = (
        f"{GOOGLE_AUTH_URL}?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&scope=openid%20email%20profile"
        f"&access_type=offline"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Login failed", 400

    # 交換 Token
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token_res = requests.post(GOOGLE_TOKEN_URL, data=token_data)
    token_json = token_res.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return f"Token exchange failed: {token_json}", 400

    # 取得使用者資訊
    headers = {"Authorization": f"Bearer {access_token}"}
    user_res = requests.get(GOOGLE_USERINFO_URL, headers=headers)
    user_info = user_res.json()

    # 存 Session
    session["user"] = user_info
    return f"登入成功！歡迎 {user_info.get('email')}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
