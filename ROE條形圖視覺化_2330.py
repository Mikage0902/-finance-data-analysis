import pandas as pd
import matplotlib.pyplot as plt

# 讀取數據
data = pd.read_excel("2330歷年經營績效.xlsx")

# 修正列名
data.rename(columns={"ROE\n(%)": "ROE"}, inplace=True)

# 刪除第二行數據
data = data.drop(index=1)

# 清洗數據，確保數值類型
data['ROE'] = pd.to_numeric(data['ROE'], errors='coerce')
data['年度'] = pd.to_numeric(data['年度'], errors='coerce')

# 移除包含 NaN 的行
data = data.dropna(subset=['ROE', '年度'])

# 確認數據
print(data.dtypes)
print(data.head())

# 設定繪圖的參數
plt.rcParams.update({
    'font.size': 10,
    "font.family": ['sans-serif', "Microsoft JhengHei"]  # 字型
})

# 繪製條形圖
plt.figure(figsize=(10, 6))
plt.bar(data['年度'], data['ROE'], color='skyblue')

# 添加標題和標籤
plt.title("年度 ROE 條形圖", fontsize=16)
plt.xlabel("年度", fontsize=12)
plt.ylabel("ROE (%)", fontsize=12)
plt.xticks(rotation=45)

# 顯示圖表
plt.tight_layout()
plt.show()
