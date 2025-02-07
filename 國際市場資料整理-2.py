import pandas as pd

# 讀取數據
df = pd.read_csv("combined_market_data_2.csv")

# 重命名欄位


def rename_columns(columns):
    renamed_columns = []
    for col in columns:
        if col in ['TNX', 'TYX', 'Gold', 'USDCNY', 'USDEUR', 'USDGBP', 'USDJPY']:  # 需要更改的欄位
            renamed_columns.append('asset_ticker')
        else:
            renamed_columns.append(col)
    return renamed_columns


# 應用名稱映射函數
new_column_names = rename_columns(df.columns)
df.columns = new_column_names

df.to_csv("combined_market_data_3.csv")
