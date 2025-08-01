# app.py
# --------------------------
# 門市考核查詢平台 Flask 主程式
# 功能：
# 1. 讀取 data 資料夾內的 Excel 檔案
# 2. 根據使用者選擇條件查詢四個分頁資料
# 3. 輸出對應表格到前端（templates/index.html 顯示）

import os
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# --------------------------
# 1️⃣ 工具函數：讀取 Excel
# --------------------------
def load_excel_data(filename):
    """讀取指定 Excel，回傳四個 DataFrame"""
    file_path = os.path.join("data", filename)
    if not os.path.exists(file_path):
        return None

    # 讀取四個分頁
    xls = pd.ExcelFile(file_path)
    sheets = {
        "summary": pd.read_excel(xls, "門店 考核總表"),
        "performance": pd.read_excel(xls, "人效分析"),
        "manager_detail": pd.read_excel(xls, "店長副店 考核明細"),
        "staff_detail": pd.read_excel(xls, "店員儲備 考核明細")
    }
    return sheets


# --------------------------
# 2️⃣ 首頁與查詢邏輯
# --------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    selected_file = None

    # 取得 data 資料夾所有檔案清單
    files = [f for f in os.listdir("data") if f.endswith(".xlsx")]

    if request.method == "POST":
        selected_file = request.form.get("file")
        area_manager = request.form.get("area_manager", "").strip()
        dept_code = request.form.get("dept_code", "").strip()
        emp_name = request.form.get("emp_name", "").strip()

        sheets = load_excel_data(selected_file)
        if sheets:
            # 過濾四個表格
            results = {}
            for key, df in sheets.items():
                filtered_df = df.copy()

                # 依條件過濾
                if area_manager:
                    filtered_df = filtered_df[filtered_df.iloc[:, 0].astype(str).str.contains(area_manager)]
                if dept_code:
                    filtered_df = filtered_df[filtered_df.iloc[:, 1].astype(str).str.contains(dept_code)]
                if emp_name:
                    filtered_df = filtered_df[filtered_df.iloc[:, 4].astype(str).str.contains(emp_name)]

                # 百分比欄位格式化
                if key == "performance":
                    percent_cols = [8, 11, 12, 13, 14]  # 0-index 對應 I、L、M、N、O
                    for col in percent_cols:
                        filtered_df.iloc[:, col] = filtered_df.iloc[:, col].apply(
                            lambda x: f"{x*100:.1f}%" if pd.notnull(x) else x
                        )

                results[key] = filtered_df.to_dict(orient="records")

    return render_template("index.html", files=files, results=results, selected_file=selected_file)


# --------------------------
# 3️⃣ 主程式入口
# --------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
