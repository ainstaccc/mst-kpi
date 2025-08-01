import os
from flask import Flask, session, redirect, url_for, render_template
from authlib.integrations.flask_client import OAuth
 
# --------------------------
# 建立 Flask App
# --------------------------
app = Flask(__name__)

# 強制使用 SECRET_KEY（Render 環境變數設定）
app.secret_key = os.environ.get("SECRET_KEY")

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

# Render 的環境變數中需設定 GOOGLE_REDIRECT_URI
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")


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
    redirect_uri = GOOGLE_REDIRECT_URI or url_for("callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


# --------------------------
# Google OAuth 回調
# --------------------------
# --------------------------
# Google OAuth 回調
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
        except Exception:
            # 若解析失敗，退而求其次呼叫 userinfo API
            resp = oauth.google.get("userinfo")
            userinfo = resp.json() if resp else {}

        # 檢查 userinfo 是否正確
        if not userinfo or "email" not in userinfo:
            raise Exception(f"無法取得 email, 回傳內容: {userinfo}")

        # 寫入 session
        session["user"] = {"email": userinfo.get("email")}

        return redirect(url_for("index"))

    except Exception as e:
        import traceback
        print("OAuth Callback Error:", e)
        traceback.print_exc()
        return f"OAuth Callback 發生錯誤：{e}", 500



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
