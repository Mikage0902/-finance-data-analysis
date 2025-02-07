import streamlit as st
import pandas as pd
from datetime import datetime, date
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import os

# 設定中文字體，避免顯示亂碼
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 設定主題
st.title("專案實作5")

# 讀取股票檔案
df = pd.read_csv("股價及技術指標_.csv")

# 確保日期欄位格式正確
df['date'] = pd.to_datetime(df['date'])
# 確保股票代號為字串格式
df['Stock_Code'] = df['Stock_Code'].astype(str)

# 建立兩欄布局
col1, col2 = st.columns([2, 1])

with col1:
    # 設定輸入股票
    stock_code = st.text_input("請輸入股票代號")

with col2:
    # 修改圖表類型選項
    chart_type = st.selectbox(
        "選擇圖表類型",
        ["K線圖", "走勢圖"]
    )

# 設定日期範圍的最小值和最大值
min_date = df['date'].min().date()
max_date = df['date'].max().date()
default_start = date(2015, 1, 1)
default_end = date(2015, 1, 31)

# 建立日期選擇器
date_range = st.date_input(
    "選擇顯示日期區間",
    value=(default_start, default_end),
    min_value=min_date,
    max_value=max_date,
    format="YYYY-MM-DD"
)

# 顯示圖表按鈕
if st.button("顯示圖表"):
    if stock_code:
        try:
            # 篩選特定股票和日期範圍的資料
            mask = (df['Stock_Code'] == stock_code) & \
                (df['date'].dt.date >= date_range[0]) & \
                (df['date'].dt.date <= date_range[1])
            filtered_df = df[mask]

            if len(filtered_df) > 0:
                if chart_type == "K線圖":
                    # 準備 mplfinance 所需的資料格式
                    filtered_df = filtered_df.set_index('date')
                    filtered_df.index.name = 'Date'
                    # 重命名欄位以符合 mplfinance 的要求
                    filtered_df = filtered_df.rename(columns={
                        'open': 'Open',
                        'high': 'High',
                        'low': 'Low',
                        'close': 'Close',
                        'volume': 'Volume'
                    })

                    # 設定K線圖樣式
                    mc = mpf.make_marketcolors(up='r', down='g',
                                               edge='inherit',
                                               wick='inherit',
                                               volume='in',
                                               ohlc='inherit')
                    s = mpf.make_mpf_style(marketcolors=mc)

                    # 創建 RSI 附圖
                    ap = [
                        mpf.make_addplot(filtered_df['RSI'], panel=2, ylabel='RSI',
                                         ylim=(0, 100), color='blue'),
                        # 添加 RSI 的超買超賣線
                        mpf.make_addplot([70] * len(filtered_df), panel=2,
                                         color='red', linestyle='--', width=0.5),
                        mpf.make_addplot([30] * len(filtered_df), panel=2,
                                         color='green', linestyle='--', width=0.5)
                    ]

                    # 繪製K線圖與RSI
                    fig, axes = mpf.plot(filtered_df,
                                         type='candle',
                                         volume=True,
                                         style=s,
                                         figsize=(12, 10),
                                         title=f'\n{stock_code} K線圖與RSI',
                                         addplot=ap,
                                         returnfig=True,
                                         panel_ratios=(6, 2, 2))  # 調整主圖、成交量和RSI的比例

                    # 調整布局
                    plt.tight_layout()
                    st.pyplot(fig)

                elif chart_type == "走勢圖":
                    # 繪製走勢圖
                    fig, ax = plt.subplots(figsize=(12, 6))

                    # 繪製收盤價走勢
                    ax.plot(filtered_df['date'],
                            filtered_df['close'], label='收盤價')

                    # 設定圖表格式
                    ax.set_title(f'{stock_code} 走勢圖')
                    ax.set_xlabel('日期')
                    ax.set_ylabel('價格')
                    ax.grid(True)
                    ax.legend()

                    # 設定x軸日期格式
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    st.pyplot(fig)

            else:
                st.warning(
                    f"在 {date_range[0]} 到 {date_range[1]} 期間內無 {stock_code} 的交易資料")
                # 顯示資料範圍供參考
                st.info(f"資料庫中 {stock_code} 的資料範圍為：\n"
                        f"從 {df[df['Stock_Code']==stock_code]['date'].min().date()} "
                        f"到 {df[df['Stock_Code']==stock_code]['date'].max().date()}")

        except Exception as e:
            st.error(f"發生錯誤: {str(e)}")
    else:
        st.warning("請輸入股票代號")

# 顯示資料狀態（可選的除錯資訊）
if st.checkbox("顯示資料庫資訊"):
    st.write("資料庫中的前幾筆資料：")
    st.write(df.head())
    st.write("資料型態：")
    st.write(df.dtypes)

# 建立基本面分析區段
st.subheader("基本面分析")
# 設定圖表類型下拉選單
chart_type_1 = st.selectbox(
    "選擇基本面圖表類型",
    ["年度ROE條形圖", "EPS成長趨勢圖"]
)
# 使用一般的 button，但給予不同的標籤
if st.button("顯示基本面圖表"):  # 改用標準的 button 方法
    if chart_type_1 == "年度ROE條形圖":
        st.image("螢幕擷取畫面 2024-12-31 170451.png")
    elif chart_type_1 == "EPS成長趨勢圖":
        st.image("螢幕擷取畫面 2024-12-31 172635.png")

# 建立籌碼面分析區段
st.subheader("籌碼面分析")
# 設定圖表類型下拉選單
chart_type_2 = st.selectbox(
    "選擇籌碼面圖表類型",
    ["三大法人買賣超金額分布圖", "法人持股變化"]
)
if st.button("顯示籌碼面圖表"):  # 改用標準的 button 方法
    if chart_type_2 == "三大法人買賣超金額分布圖":
        st.image("螢幕擷取畫面 2025-01-01 215803.png")
    elif chart_type_2 == "法人持股變化":
        st.image("螢幕擷取畫面 2025-01-01 215521.png")
