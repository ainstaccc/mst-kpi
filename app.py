import os
from flask import Flask, redirect, url_for, request, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "your-secret-key")

# Google OAuth 設定
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "https://mst-kpi.onrender.com/callback")
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

# ======================
# 1️⃣ 首頁
# ======================
@app.route("/")
def index():
    user = session.get("user")
    if user:
        return f"<h1>歡迎，{user['email']}</h1><br><a href='/logout'>登出</a>"
    else:
        return """
        <h1>米斯特 門市考核查詢系統</h1>
        <p>請以 Gmail 帳號登入：</p>
        <a href="/login/google"><button>使用 Google 帳號登入</button></a>
        """

# ======================
# 2️⃣ Google OAuth 登入
# ======================
@app.route("/login")
def login():
    try:
        print("DEBUG: GOOGLE_REDIRECT_URI =", GOOGLE_REDIRECT_URI)
        auth_url = (
            f"{GOOGLE_AUTH_URL}?response_type=code"
            f"&client_id={GOOGLE_CLIENT_ID}"
            f"&redirect_uri={GOOGLE_REDIRECT_URI}"
            f"&scope=openid%20email%20profile"
            f"&access_type=offline"
        )
        return redirect(auth_url)
    except Exception as e:
        print("ERROR in /login:", e)
        return "Login error", 500

# 讓 /login/google 也能用（解決 404）
@app.route("/login/google")
def login_google():
    return redirect("/login")

# ======================
# 3️⃣ Google OAuth 回調
# ======================
@app.route("/callback")
def callback():
    try:
        code = request.args.get("code")
        if not code:
            return "No code received", 400

        # 交換 token
        token_data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        token_res = requests.post(GOOGLE_TOKEN_URL, data=token_data)
        token_json = token_res.json()
        print("DEBUG: Token Response =", token_json)

        # 拿使用者資料
        headers = {"Authorization": f"Bearer {token_json.get('access_token')}"}
        userinfo_res = requests.get(GOOGLE_USERINFO_URL, headers=headers)
        userinfo = userinfo_res.json()
        print("DEBUG: User Info =", userinfo)

        # 存到 session
        session["user"] = userinfo
        return redirect(url_for("index"))

    except Exception as e:
        print("ERROR in /callback:", e)
        return "Callback error", 500

# ======================
# 4️⃣ 登出
# ======================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

# ======================
# 5️⃣ 啟動（本地測試用）
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
