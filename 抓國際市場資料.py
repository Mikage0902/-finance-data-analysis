import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 外匯匯率


def get_comprehensive_market_data():
    symbols = [
        '^TNX',    # 10年期国债收益率
        '^TYX',    # 30年期国债收益率
    ]
    market_data = yf.download(
        symbols,
        period="10y",
        interval="1d",
        actions=True,
        rounding=True
    )
    return market_data

# 黄金和贵金属


def get_precious_metals():
    metals = [
        'GC=F'     # 黄金期货
    ]
    metals_data = yf.download(
        metals,
        period="10y",
        interval="1d",
        actions=True,
        rounding=True
    )
    return metals_data


def get_major_forex_data():
    forex_pairs = [
        'USDJPY=X',  # 美元/日元
        'USDCNY=X',  # 美元/人民幣
        'USDEUR=X',  # 美元/歐元
        'USDGBP=X'   # 美元/英鎊
    ]

    # 直接下載所有匯率對的數據
    forex_data = yf.download(
        forex_pairs,
        period="10y",
        interval="1d",
        rounding=True
    )

    return forex_data

# 综合数据收集並保存


def collect_and_save_market_data():
    # 獲取數據
    forex_data = get_major_forex_data()
    metals_data = get_precious_metals()
    treasury_data = get_comprehensive_market_data()

    # 處理外匯數據的多層級列名
    forex_data.columns = [
        f'Forex_{pair}_{col}' for pair, col in forex_data.columns]

    # 處理貴金屬數據
    metals_data.columns = [f'Gold_{col}' for col in metals_data.columns]

    # 處理國債數據
    treasury_data.columns = [
        f'Treasury_{col}' for col in treasury_data.columns]

    # 重設索引，保留日期列
    forex_data = forex_data.reset_index()
    metals_data = metals_data.reset_index()
    treasury_data = treasury_data.reset_index()

    # 使用日期合併所有數據
    merged_data = pd.merge(forex_data, metals_data, on='Date', how='outer')
    merged_data = pd.merge(merged_data, treasury_data, on='Date', how='outer')

    # 按日期排序
    merged_data = merged_data.sort_values('Date')

    # 保存合併後的數據
    merged_data.to_csv('combined_market_data.csv', index=False)

    # 打印合併後的數據信息
    print("\nCombined Data Info:")
    print(merged_data.info())

    # 打印前幾行數據預覽
    print("\nData Preview:")
    print(merged_data.head())

    return merged_data


# 運行數據收集和保存
market_data = collect_and_save_market_data()
