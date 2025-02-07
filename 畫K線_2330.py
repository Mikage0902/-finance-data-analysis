import pandas as pd
import talib
from talib.abstract import EMA, RSI, STOCH
import mplfinance as mpf

data = pd.read_csv("股價及技術指標_.csv")

# =============================================================================
# # 鎖定特定股票代號
# target_stock_2330 = '2330'
# filtered_data = data[data['Stock_Code'] == target_stock_2330]
# =============================================================================


def filter_stock(df, stock_code):
    """
    從DataFrame中過濾出指定的股票代號的資料

    Parameters:
    df (pandas.DataFrame): 原始資料框架
    stock_code (str): 要篩選的股票代號

    Returns:
    pandas.DataFrame: 只包含指定股票的資料框架
    """
    # 確保股票代號欄位的值都是字串類型
    if 'Stock_Code' in df.columns:
        df['Stock_Code'] = df['Stock_Code'].astype(str)

    # 過濾指定股票
    filtered_df = df[df['Stock_Code'] == str(stock_code)].copy()

    # 重設索引
    filtered_df = filtered_df.reset_index(drop=True)

    return filtered_df


# 使用範例：
"""
# 假設你有以下資料
data = {
    'stock_code': ['2330', '2317', '2454', '2330', '2317'],
    'date': ['2024-01-01', '2024-01-01', '2024-01-01', '2024-01-02', '2024-01-02'],
    'price': [500, 100, 200, 510, 102]
}
df = pd.DataFrame(data)

# 篩選出台積電(2330)的資料
tsmc_df = filter_stock(df, '2330')
"""
# 鎖定特定股票代號 (2330)
target_stock_2330 = filter_stock(data, "2330")
target_stock_2330.rename(columns={"open": "Open",
                                  "high": "High",
                                  "low": "Low",
                                  "close": "Close",
                                  "volume": "Volume"}, inplace=True)

target_stock_2330['date'] = pd.to_datetime(
    target_stock_2330['date'], format='%Y-%m-%d')
target_stock_2330 = target_stock_2330.set_index('date')  # 將日期設為index

# 設定紅漲綠跌
mcolor = mpf.make_marketcolors(up='r', down='g')
mstyle = mpf.make_mpf_style(base_mpf_style='yahoo',
                            marketcolors=mcolor)

# 計算EMA分為五日、月線
target_stock_2330["EMA5"] = talib.EMA(target_stock_2330['Close'], timeperiod=5)
target_stock_2330["EMA20"] = talib.EMA(
    target_stock_2330['Close'], timeperiod=20)

# 計算RSI
target_stock_2330["rsi_6"] = talib.RSI(
    target_stock_2330['Close'], timeperiod=6)
target_stock_2330["rsi_12"] = talib.RSI(
    target_stock_2330['Close'], timeperiod=12)

addp = []
addp.append(mpf.make_addplot(target_stock_2330["EMA5"]))
addp.append(mpf.make_addplot(target_stock_2330["EMA20"]))
addp.append(mpf.make_addplot(target_stock_2330["rsi_6"], panel=2))
addp.append(mpf.make_addplot(target_stock_2330["rsi_12"], panel=2))


# 創建超買超賣線的數據
overbought = [70] * len(target_stock_2330)  # 超買線
oversold = [30] * len(target_stock_2330)    # 超賣線
# 添加超買超賣線
addp.append(mpf.make_addplot(overbought, panel=2,
            color='r', linestyle='--'))  # 紅色虛線
addp.append(mpf.make_addplot(oversold, panel=2,
            color='g', linestyle='--'))    # 綠色虛線

mpf.plot(target_stock_2330,
         type='candle',
         style=mstyle,
         volume=True,
         addplot=addp)  # 資料太多會跳錯誤訊息但程式能執行並跑出圖片


# 鎖定特定股票代號 (2449)
target_stock_2449 = filter_stock(data, "2449")
