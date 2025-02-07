import pandas as pd

df = pd.read_csv("combined_market_data.csv")
df.set_index('Date', inplace=True)


def reorder_columns(df):
    new_order = [
        # Treasury TNX
        "Treasury_('Open', '^TNX')", "Treasury_('High', '^TNX')", "Treasury_('Low', '^TNX')",
        "Treasury_('Close', '^TNX')", "Treasury_('Adj Close', '^TNX')", "Treasury_('Volume', '^TNX')",
        "Treasury_('Dividends', '^TNX')", "Treasury_('Stock Splits', '^TNX')",

        # Treasury TYX
        "Treasury_('Open', '^TYX')", "Treasury_('High', '^TYX')", "Treasury_('Low', '^TYX')",
        "Treasury_('Close', '^TYX')", "Treasury_('Adj Close', '^TYX')", "Treasury_('Volume', '^TYX')",
        "Treasury_('Dividends', '^TYX')", "Treasury_('Stock Splits', '^TYX')",

        # Gold
        "Gold_Open", "Gold_High", "Gold_Low", "Gold_Close", "Gold_Adj Close",
        "Gold_Volume", "Gold_Dividends", "Gold_Stock Splits",

        # Forex CNY
        "Forex_Open_USDCNY=X", "Forex_High_USDCNY=X", "Forex_Low_USDCNY=X",
        "Forex_Close_USDCNY=X", "Forex_Adj Close_USDCNY=X", "Forex_Volume_USDCNY=X",

        # Forex EUR
        "Forex_Open_USDEUR=X", "Forex_High_USDEUR=X", "Forex_Low_USDEUR=X",
        "Forex_Close_USDEUR=X", "Forex_Adj Close_USDEUR=X", "Forex_Volume_USDEUR=X",

        # Forex GBP
        "Forex_Open_USDGBP=X", "Forex_High_USDGBP=X", "Forex_Low_USDGBP=X",
        "Forex_Close_USDGBP=X", "Forex_Adj Close_USDGBP=X", "Forex_Volume_USDGBP=X",

        # Forex JPY
        "Forex_Open_USDJPY=X", "Forex_High_USDJPY=X", "Forex_Low_USDJPY=X",
        "Forex_Close_USDJPY=X", "Forex_Adj Close_USDJPY=X", "Forex_Volume_USDJPY=X"
    ]
    return df[new_order]


# Usage:
df = reorder_columns(df)
# =============================================================================
# # 列出所有欄位順序
# for col in df.columns:
#     print(col)
# =============================================================================

# df.to_csv("測試.csv")
# 新增 "TNX" 欄位，並填入字串 "TNX"
df.insert(loc=df.columns.get_loc("Treasury_('Open', '^TNX')"),
          column='TNX', value='TNX')
# 更改欄位名稱
rename_map = {
    "Treasury_('Open', '^TNX')": "Open",
    "Treasury_('High', '^TNX')": "High",
    "Treasury_('Low', '^TNX')": "Low",
    "Treasury_('Close', '^TNX')": "Close",
    "Treasury_('Adj Close', '^TNX')": "Adj Close",
    "Treasury_('Volume', '^TNX')": "Volume",
    "Treasury_('Dividends', '^TNX')": "Dividends",
    "Treasury_('Stock Splits', '^TNX')": "Stock Splits"
}
# 重新命名欄位
df.rename(columns=rename_map, inplace=True)

# 新增 "TYX" 欄位 (在某欄位前面新增欄位)
df.insert(
    loc=df.columns.get_loc("Treasury_('Open', '^TYX')"),
    # 獲取 "Treasury_('Open', '^TYX')" 的索引位置
    column="TYX",  # 欄位名稱
    value="TYX"  # 填入的值
)

# 更改欄位名稱
rename_map = {
    "Treasury_('Open', '^TYX')": "Open",
    "Treasury_('High', '^TYX')": "High",
    "Treasury_('Low', '^TYX')": "Low",
    "Treasury_('Close', '^TYX')": "Close",
    "Treasury_('Adj Close', '^TYX')": "Adj Close",
    "Treasury_('Volume', '^TYX')": "Volume",
    "Treasury_('Dividends', '^TYX')": "Dividends",
    "Treasury_('Stock Splits', '^TYX')": "Stock Splits"
}
# 重新命名欄位
df.rename(columns=rename_map, inplace=True)

# 新增 "Gold" 欄位 (在某欄位前面新增欄位)
df.insert(
    loc=df.columns.get_loc("Gold_Open"),
    # 獲取 "Treasury_('Open', '^TYX')" 的索引位置
    column="Gold",  # 欄位名稱
    value="Gold"  # 填入的值
)

# 更改欄位名稱
rename_map = {
    "Gold_Open": "Open",
    "Gold_High": "High",
    "Gold_Low": "Low",
    "Gold_Close": "Close",
    "Gold_Adj Close": "Adj Close",
    "Gold_Volume": "Volume",
    "Gold_Dividends": "Dividends",
    "Gold_Stock Splits": "Stock Splits"
}
# 重新命名欄位
df.rename(columns=rename_map, inplace=True)

# 新增 "USDCNY" 欄位 (在某欄位前面新增欄位)
df.insert(
    loc=df.columns.get_loc("Forex_Open_USDCNY=X"),
    # 獲取 "Treasury_('Open', '^TYX')" 的索引位置
    column="USDCNY",  # 欄位名稱
    value="USDCNY"  # 填入的值
)

# 更改欄位名稱
rename_map = {
    "Forex_Open_USDCNY=X": "Open",
    "Forex_High_USDCNY=X": "High",
    "Forex_Low_USDCNY=X": "Low",
    "Forex_Close_USDCNY=X": "Close",
    "Forex_Adj Close_USDCNY=X": "Adj Close",
    "Forex_Volume_USDCNY=X": "Volume"
}
# 重新命名欄位
df.rename(columns=rename_map, inplace=True)

# 新增 "USDEUR" 欄位 (在某欄位前面新增欄位)
df.insert(
    loc=df.columns.get_loc("Forex_Open_USDEUR=X"),
    # 獲取 "Treasury_('Open', '^TYX')" 的索引位置
    column="USDEUR",  # 欄位名稱
    value="USDEUR"  # 填入的值
)

# 更改欄位名稱
rename_map = {
    "Forex_Open_USDEUR=X": "Open",
    "Forex_High_USDEUR=X": "High",
    "Forex_Low_USDEUR=X": "Low",
    "Forex_Close_USDEUR=X": "Close",
    "Forex_Adj Close_USDEUR=X": "Adj Close",
    "Forex_Volume_USDEUR=X": "Volume"
}
# 重新命名欄位
df.rename(columns=rename_map, inplace=True)

# 新增 "USDGBP" 欄位 (在某欄位前面新增欄位)
df.insert(
    loc=df.columns.get_loc("Forex_Open_USDGBP=X"),
    # 獲取 "Treasury_('Open', '^TYX')" 的索引位置
    column="USDGBP",  # 欄位名稱
    value="USDGBP"  # 填入的值
)

# 更改欄位名稱
rename_map = {
    "Forex_Open_USDGBP=X": "Open",
    "Forex_High_USDGBP=X": "High",
    "Forex_Low_USDGBP=X": "Low",
    "Forex_Close_USDGBP=X": "Close",
    "Forex_Adj Close_USDGBP=X": "Adj Close",
    "Forex_Volume_USDGBP=X": "Volume"
}
# 重新命名欄位
df.rename(columns=rename_map, inplace=True)

# 新增 "USDJPY" 欄位 (在某欄位前面新增欄位)
df.insert(
    loc=df.columns.get_loc("Forex_Open_USDJPY=X"),
    # 獲取 "Treasury_('Open', '^TYX')" 的索引位置
    column="USDJPY",  # 欄位名稱
    value="USDJPY"  # 填入的值
)

# 更改欄位名稱
rename_map = {
    "Forex_Open_USDJPY=X": "Open",
    "Forex_High_USDJPY=X": "High",
    "Forex_Low_USDJPY=X": "Low",
    "Forex_Close_USDJPY=X": "Close",
    "Forex_Adj Close_USDJPY=X": "Adj Close",
    "Forex_Volume_USDJPY=X": "Volume"
}
# 重新命名欄位
df.rename(columns=rename_map, inplace=True)

df.to_csv("combined_market_data_2.csv")
