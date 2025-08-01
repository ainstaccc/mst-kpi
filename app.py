from flask import Flask, session, redirect, url_for
import os

app = Flask(__name__)

# 強制使用 SECRET_KEY（Render 環境變數設定）
app.secret_key = os.environ.get("SECRET_KEY")

@app.route("/")
def home():
    user = session.get('user')
    if user:
        return f"<h1>👋 歡迎 {user['email']}</h1>"
    return "<h1>Hello, Render!</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
