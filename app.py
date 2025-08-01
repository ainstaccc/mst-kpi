# app.py
# ------------------------------
# 這是一個最簡單的 Flask 範例，包含首頁與登入頁
# ------------------------------

from flask import Flask, render_template

app = Flask(__name__)

# 首頁路由
@app.route("/")
def index():
    files = ["檔案A", "檔案B", "檔案C"]  # 模擬檔案列表
    results = ["結果1", "結果2", "結果3"]  # 模擬結果列表
    selected_file = None
    return render_template("index.html", files=files, results=results, selected_file=selected_file)

# 登入路由
@app.route("/login")
def login():
    return "這是登入頁面，之後可以放 Google OAuth 登入"

if __name__ == "__main__":
    app.run(debug=True)
