# app.py
# -----------------------------
# 這是一個簡單的 Flask Web App
# 功能：
# 1. 首頁顯示 index.html
# 2. 提供 /login 測試頁面避免錯誤
# -----------------------------

from flask import Flask, render_template

app = Flask(__name__)

# 首頁路由
@app.route("/")
def index():
    # 這裡模擬傳給模板的變數
    files = []               # 檔案清單
    results = []             # 結果列表
    selected_file = None     # 選擇的檔案

    return render_template("index.html", files=files, results=results, selected_file=selected_file)

# 登入路由（目前是假的，只回傳文字）
@app.route("/login")
def login():
    return "這是登入頁面，之後可以接 Google OAuth"

# 主程式入口
if __name__ == "__main__":
    app.run(debug=True)
