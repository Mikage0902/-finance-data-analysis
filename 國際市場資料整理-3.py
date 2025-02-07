import pandas as pd
import re
import numpy as np

# 讀取數據
df = pd.read_csv("combined_market_data_3.csv")

# Replace NaN values with 0
data_filled = df.fillna(0)
# 要把檔案欄位後續的123都去掉
# print(data_filled.columns)


def rename_duplicate_columns(df):
    """
    重新命名含數字後綴的重複欄位名稱，移除所有後綴

    Parameters:
    df (pandas.DataFrame): 要重新命名欄位的 DataFrame

    Returns:
    pandas.DataFrame: 重新命名欄位後的 DataFrame
    """
    # 建立新的欄位名稱映射
    column_mapping = {}

    # 遍歷所有欄位
    for col in df.columns:
        # 使用正規表達式移除 .數字 後綴
        new_col = re.sub(r'\.\d+$', '', col)
        column_mapping[col] = new_col

    # 重新命名 DataFrame 的欄位
    return df.rename(columns=column_mapping)


data_filled_1 = rename_duplicate_columns(data_filled)


def merge_duplicate_columns(df):
    """
    將重複的欄位向下合併並設定多重索引

    Parameters:
    df (pandas.DataFrame): 含有重複欄位的 DataFrame

    Returns:
    pandas.DataFrame: 合併後並設定多重索引的 DataFrame
    """
    # 首先重新命名欄位，移除數字後綴
    renamed_df = df.rename(columns=lambda x: x.split('.')[0])

    # 獲取所有唯一的欄位名稱
    unique_columns = ['Date', 'asset_ticker', 'Open', 'High', 'Low', 'Close',
                      'Adj Close', 'Volume', 'Dividends', 'Stock Splits']

    # 創建一個空的 list 來存儲所有資料
    all_data = []

    # 遍歷每一行
    for idx, row in df.iterrows():
        date = row['Date']  # 保存日期

        # 找出這一行中所有的資產資料
        for i in range(7):  # 假設有7個資產（根據原始數據的後綴 .1 到 .6）
            # 確定後綴
            suffix = '' if i == 0 else f'.{i}'

            # 檢查是否存在這個資產的資料（用 asset_ticker 來檢查）
            ticker_col = f'asset_ticker{suffix}'
            if ticker_col in df.columns and not pd.isna(row[ticker_col]):
                # 創建這個資產的資料字典
                asset_data = {
                    'Date': pd.to_datetime(date),  # 確保日期格式正確
                    'asset_ticker': row[f'asset_ticker{suffix}'],
                    'Open': row[f'Open{suffix}'],
                    'High': row[f'High{suffix}'],
                    'Low': row[f'Low{suffix}'],
                    'Close': row[f'Close{suffix}'],
                    'Adj Close': row[f'Adj Close{suffix}'],
                    'Volume': row[f'Volume{suffix}'],
                    'Dividends': row[f'Dividends{suffix}'] if f'Dividends{suffix}' in df.columns else 0,
                    'Stock Splits': row[f'Stock Splits{suffix}'] if f'Stock Splits{suffix}' in df.columns else 0
                }
                all_data.append(asset_data)

    # 創建新的 DataFrame
    merged_df = pd.DataFrame(all_data)

    # 確保欄位順序正確
    merged_df = merged_df[unique_columns]

    # 排序資料
    merged_df = merged_df.sort_values(['Date', 'asset_ticker'])

    # 設定多重索引
    merged_df = merged_df.set_index(['Date', 'asset_ticker'])

    return merged_df


merged_df = merge_duplicate_columns(data_filled)

merged_df.to_csv("combined_market_data_4.csv")
