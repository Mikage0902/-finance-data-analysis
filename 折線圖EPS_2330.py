import pandas as pd
import matplotlib.pyplot as plt

# 讀取數據
data = pd.read_excel("2330歷年經營績效.xlsx")

# 刪除第0、1行數據
data = data.drop(index=0)
data = data.drop(index=1)

# 修正列名（如果列名中有換行符等問題）
data.rename(columns={"EPS(元)": "EPS"}, inplace=True)

# 確保數據按年度排序（如果未排序）
data = data.sort_values(by="年度")

# 轉換 EPS 列為數值型，非數值將被轉換為 NaN
data['EPS'] = pd.to_numeric(data['EPS'], errors='coerce')

# 刪除 EPS 或 年度 中有 NaN 的行
data = data.dropna(subset=['EPS', '年度'])

# 計算 EPS 成長率
data['EPS Growth Rate (%)'] = data['EPS'].pct_change() * 100

# 刪除第一行，因為第一行無法計算成長率（會是 NaN）
data = data.dropna(subset=['EPS Growth Rate (%)'])

# 確保數據的類型正確
data['年度'] = pd.to_numeric(data['年度'], errors='coerce')
data['EPS Growth Rate (%)'] = pd.to_numeric(
    data['EPS Growth Rate (%)'], errors='coerce')

# 設定繪圖的參數
plt.rcParams.update({
    'font.size': 10,
    "font.family": ['sans-serif', "Microsoft JhengHei"]  # 字型
})

# 繪製折線圖
plt.figure(figsize=(10, 6))
plt.plot(data['年度'], data['EPS Growth Rate (%)'], marker='o',
         color='b', linestyle='-', linewidth=2, markersize=6)

# 添加標題和標籤
plt.title("EPS 成長率趨勢", fontsize=16)
plt.xlabel("年度", fontsize=12)
plt.ylabel("EPS 成長率 (%)", fontsize=12)

# 顯示圖表
plt.grid(True)  # 顯示網格線
plt.tight_layout()
plt.show()
