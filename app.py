import os
from flask import Flask, session, redirect, url_for, render_template
from authlib.integrations.flask_client import OAuth
from flask_session import Session  # ✅ 新增：用於 Server-Side Session

# --------------------------
# 建立 Flask App
# --------------------------
app = Flask(__name__)

# 設定 SECRET_KEY（Render 環境變數）
app.secret_key = os.environ.get("SECRET_KEY")

# --------------------------
# 啟用 Server-Side Session
# --------------------------
# 使用伺服器端存儲 Session 避免 Render 重啟導致的 state 錯誤
app.config["SESSION_TYPE"] = "filesystem"  # 檔案系統存儲
app.config["SESSION_PERMANENT"] = False    # 不永久保存
Session(app)

# --------------------------
# Google OAuth 設定
# --------------------------
oauth = OAuth(app)
oauth.register(
    name="google",
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# --------------------------
# 首頁
# --------------------------
@app.route("/")
def index():
    """
    首頁：如果已登入則顯示使用者 Email，否則顯示登入按鈕
    """
    user = session.get("user")
    if user:
        return render_template("index.html", email=user.get("email"))
    return render_template("index.html", email=None)

# --------------------------
# 登入 Google
# --------------------------
@app.route("/login")
def login():
    """
    點擊登入後，導向 Google OAuth
    """
    # 使用 url_for 產生完整 HTTPS 回調網址
    redirect_uri = url_for("callback", _external=True, _scheme="https")
    return oauth.google.authorize_redirect(redirect_uri)

# --------------------------
# Google OAuth 回調（含錯誤顯示）
# --------------------------
@app.route("/callback")
def callback():
    try:
        # 取得 token
        token = oauth.google.authorize_access_token()

        # 嘗試解析 ID Token
        userinfo = None
        try:
            userinfo = oauth.google.parse_id_token(token)
        except Exception as e:
            print("Parse ID Token Error:", e)
            # 若解析失敗，退而求其次呼叫 userinfo API
            resp = oauth.google.get("userinfo")
            userinfo = resp.json() if resp else {}

        # 檢查 userinfo 是否正確
        if not userinfo or "email" not in userinfo:
            return f"<h2>OAuth 錯誤</h2><p>無法取得 email，回傳內容:</p><pre>{userinfo}</pre>"

        # 寫入 session
        session["user"] = {"email": userinfo.get("email")}

        return redirect(url_for("index"))

    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        return f"<h2>OAuth Callback 發生錯誤</h2><pre>{error_detail}</pre>", 500

# --------------------------
# 登出
# --------------------------
@app.route("/logout")
def logout():
    """
    登出並清空 session
    """
    session.clear()
    return redirect(url_for("index"))

# --------------------------
# Render 運行入口
# --------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
