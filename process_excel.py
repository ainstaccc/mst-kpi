#!/usr/bin/env python3
import pandas as pd
import json
import os
import numpy as np

def process_excel_data():
    excel_path = '/home/ubuntu/downloads/2025.06門市-考核總表.xlsx'
    
    # Read all sheets
    excel_data = pd.read_excel(excel_path, sheet_name=None)
    
    # Process 門店 考核總表
    summary_df = pd.read_excel(excel_path, sheet_name='門店 考核總表', header=1)
    summary_df = summary_df.dropna(subset=['考核分類'])  # Remove empty rows
    # Replace NaN with None for JSON serialization
    summary_df = summary_df.replace({np.nan: None})
    summary_data = summary_df.to_dict('records')
    
    # Process 人效分析
    efficiency_df = pd.read_excel(excel_path, sheet_name='人效分析', header=1)
    efficiency_df = efficiency_df.dropna(subset=['區主管'])  # Remove empty rows
    efficiency_df = efficiency_df.replace({np.nan: None})
    efficiency_data = efficiency_df.to_dict('records')
    
    # Process 店長副店 考核明細
    manager_detail_df = pd.read_excel(excel_path, sheet_name='店長副店 考核明細', header=1)
    manager_detail_df = manager_detail_df.dropna(subset=['部門編號'])  # Remove empty rows
    manager_detail_df = manager_detail_df.replace({np.nan: None})
    manager_detail_data = manager_detail_df.to_dict('records')
    
    # Process 店員儲備 考核明細
    staff_detail_df = pd.read_excel(excel_path, sheet_name='店員儲備 考核明細', header=1)
    staff_detail_df = staff_detail_df.dropna(subset=['部門編號'])  # Remove empty rows
    staff_detail_df = staff_detail_df.replace({np.nan: None})
    staff_detail_data = staff_detail_df.to_dict('records')
    
    # Combine all data
    all_data = {
        'summary': summary_data,
        'efficiency': efficiency_data,
        'manager_detail': manager_detail_data,
        'staff_detail': staff_detail_data
    }
    
    # Save to JSON file
    output_path = '/home/ubuntu/mst-kpi-platform/public/data.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"Data processed and saved to {output_path}")
    print(f"Summary records: {len(summary_data)}")
    print(f"Efficiency records: {len(efficiency_data)}")
    print(f"Manager detail records: {len(manager_detail_data)}")
    print(f"Staff detail records: {len(staff_detail_data)}")

if __name__ == "__main__":
    process_excel_data()

