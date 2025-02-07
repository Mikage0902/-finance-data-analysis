import yfinance as yf
from talib.abstract import RSI
import talib
import pandas as pd
import os
import time

# 空DataFrame紀錄最後結果
all_stock_data = pd.DataFrame()

# 創建一個空列表來記錄無數據的股票
no_data_stocks = []

# 開始時間
start_time = time.time()
print(start_time)
# 使用os.path.join拼接路徑
file_path = os.path.join(r"E:\凱衛學院", "專案一_爬蟲", "類股統整.xlsx")

# 讀取Excel檔案
df = pd.read_excel(file_path)


def get_stock_data(stook_id):
    try:
        # 尝试获取股票数据
        df = yf.Ticker(stook_id)
        # period=日期範圍 (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max)
        # interval=頻率 (1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo)
        df = df.history(period="10y", interval="1d")

        # 检查数据是否为空
        if df.empty:
            print(f"股票 {stock_code} 没有数据")
            return None

        # 將資料取到小數第二位
        df = df.round(2)
        # 因抓取時間關係可能抓到未收盤資料要根據頻率刪除
        df = df.iloc[:-1]  # 刪除最後N筆資料

        df = df.reset_index()  # 將在index的日期變成欄位

        # 將股票代號設為index
        df['Stock_Code'] = stock_code
        df.set_index(['Stock_Code'], inplace=True)

        return df

    except Exception as e:
        print(f"获取 {stock_code} 数据时发生错误: {e}")
        return None


# 逐行逐列，取得股票代號欄位的資料
for index, row in df.iterrows():
    stock_code = row['代號']  # 假設欄位名稱為'代號'
    print(f"第 {index} 行的股票代號: {stock_code}")
    stock_code_str = str(stock_code)
    stook_id = stock_code_str+".tw"  # 京元電子

    data = get_stock_data(stook_id)  # stook_id  "5878.TW"
    print(data)
    if data is None:
        no_data_stocks.append(stock_code)
        continue
    data.columns = ['date', 'open',
                    'high', 'low',
                    'close', 'volume',
                    "dividends", "stock splits"]

    # 計算RSI
    data["RSI"] = RSI(data, timeperiod=7)  # 計算期間
    data["ceil"] = 70
    data["floor"] = 40

    # 計算KD指標
    # slowk: K值
    # slowd: D值
    slowk, slowd = talib.STOCH(
        high=data['high'],
        low=data['low'],
        close=data['close'],
        fastk_period=9,   # K值週期
        slowk_period=3,   # 慢速K值平滑週期
        slowd_period=3    # D值平滑週期
    )

    # 將結果加入原始DataFrame
    data['K'] = slowk
    data['D'] = slowd

    all_stock_data = pd.concat([all_stock_data, data])

# 結束時間
end_time = time.time()
execution_time = end_time - start_time
print(f"程式執行時間: {execution_time:.2f} 秒")
# 去除時區標記
all_stock_data['date'] = all_stock_data['date'].dt.tz_localize(None).dt.date
all_stock_data.to_csv("股價及技術指標_.csv")
