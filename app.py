# app.py
# ---------------------------
# 門市考核查詢平台 - Flask 後端程式
# 功能：
# 1. 讀取專案資料夾中最新的 Excel 檔
# 2. 提供查詢 API
# 3. 顯示首頁（查詢頁面）
# ---------------------------

from flask import Flask, render_template, request, jsonify
import os
import pandas as pd

app = Flask(__name__)

# 設定資料夾
DATA_FOLDER = "./data"

# 取得最新 Excel 檔案
def get_latest_excel():
    files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".xlsx")]
    if not files:
        return None
    # 按照檔名排序，最新的放最後
    files.sort()
    latest_file = files[-1]
    return os.path.join(DATA_FOLDER, latest_file)

# 讀取 Excel 分頁
def load_sheets():
    latest_excel = get_latest_excel()
    if latest_excel is None:
        return {}

    # 讀取四個指定分頁
    sheets = pd.read_excel(latest_excel, sheet_name=None)
    result = {}

    # 固定分頁名稱
    target_sheets = [
        "門店 考核總表",
        "人效分析",
        "店長副店 考核明細",
        "店員儲備 考核明細"
    ]
    for sheet_name in target_sheets:
        if sheet_name in sheets:
            result[sheet_name] = sheets[sheet_name]
        else:
            result[sheet_name] = pd.DataFrame()  # 沒資料給空表

    return result


# 首頁
@app.route("/")
def index():
    return render_template("index.html")


# 查詢 API
@app.route("/query", methods=["POST"])
def query_data():
    # 取得使用者輸入
    query_type = request.json.get("queryType", "store")  # store / manager
    filters = request.json.get("filters", {})

    sheets = load_sheets()
    if not sheets:
        return jsonify({"error": "找不到 Excel 資料"}), 400

    # 範例：直接回傳每個分頁的筆數
    response = {
        name: len(df)
        for name, df in sheets.items()
    }

    return jsonify(response)


if __name__ == "__main__":
    # Render 用的埠號設定
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
