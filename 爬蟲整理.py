from os import listdir
import pandas as pd
import os

# 空DataFrame紀錄最後結果
all_stock_performance = pd.DataFrame()

# 資料夾路徑
folder_path = r"E:\凱衛學院\專案一_爬蟲 - 複製"

# 取得資料夾內各類股
catched_stock_list = listdir(folder_path)

for file_name in catched_stock_list:
    # 將檔案名分割成"類股".".xlsx"
    s_id = file_name.split('.')

    # 只取"類股名"
    stock_id = s_id[0]

    # 檢查是否為Excel檔案
    if file_name.endswith('.xlsx'):
        # 建立完整檔案路徑
        file_path = os.path.join(folder_path, file_name)

        try:
            # 讀取Excel檔案
            stock_df = pd.read_excel(file_path)

            # 只針對數值欄位替換NaN為0
            numeric_columns = stock_df.select_dtypes(
                include=['float64', 'int64']).columns
            stock_df[numeric_columns] = stock_df[numeric_columns].fillna(0)

            # 在DataFrame中加入類股名稱欄位
            stock_df['stock_category'] = stock_id

            # 將每個類股的DataFrame合併到總DataFrame
            all_stock_performance = pd.concat(
                [all_stock_performance, stock_df], ignore_index=True)

            print(f"Successfully read {file_name}")

        except Exception as e:
            print(f"Error reading {file_name}: {e}")

# 查看合併後的結果
print(all_stock_performance)
all_stock_performance.to_excel("類股統整.xlsx")
