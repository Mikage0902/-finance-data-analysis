import pandas as pd
import matplotlib.pyplot as plt

# 讀取 Excel 檔案
file_path = '2330三大法人買賣超.xlsx'  # 替換為您的檔案路徑
sheet1_data = pd.read_excel(file_path, sheet_name='Sheet1')

# 數據清理與轉換
sheet1_data.columns = [
    "日期", "成交", "漲跌", "漲跌(%)", "成交量(張)",
    "外資買進(張)", "外資賣出(張)", "外資買賣超(張)", "外資持有(張)", "外資持股比率(%)",
    "投信買進(張)", "投信賣出(張)", "投信買賣超(張)",
    "自營商買進(張)", "自營商賣出(張)", "自營商買賣超(張)",
    "三大法人買進(張)", "三大法人賣出(張)", "三大法人買賣超(張)"
]

# 移除表頭重複行或 NaN 行
sheet1_data = sheet1_data.dropna(subset=["日期"]).reset_index(drop=True)

# 日期格式處理
sheet1_data["日期"] = pd.to_datetime(sheet1_data["日期"], format="%y/%m/%d")

# 將數字相關欄位轉換為浮點數
num_cols = [
    "外資買賣超(張)", "外資持有(張)", "投信買賣超(張)",
    "自營商買賣超(張)", "三大法人買賣超(張)"
]
sheet1_data[num_cols] = sheet1_data[num_cols].apply(
    pd.to_numeric, errors="coerce")

# 設定繪圖的參數
plt.rcParams.update({
    'font.size': 10,  # 文字大小
    "font.family": ['sans-serif', "Microsoft JhengHei"]  # 字型
})

# 繪製法人持股變化折線圖
plt.figure(figsize=(12, 6))
plt.plot(sheet1_data["日期"], sheet1_data["外資持有(張)"] / 1000,
         label="外資持股(千張)", color="blue", linewidth=2)
plt.title("法人持股變化", fontsize=16)
plt.xlabel("日期", fontsize=12)
plt.ylabel("持股量 (千張)", fontsize=12)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# 繪製三大法人買賣超金額分佈的堆疊條形圖
plt.figure(figsize=(12, 6))
plt.bar(sheet1_data["日期"], sheet1_data["外資買賣超(張)"] /
        1000, label="外資", color="blue")
plt.bar(sheet1_data["日期"], sheet1_data["投信買賣超(張)"] / 1000,
        bottom=sheet1_data["外資買賣超(張)"] / 1000, label="投信", color="orange")
plt.bar(
    sheet1_data["日期"],
    sheet1_data["自營商買賣超(張)"] / 1000,
    bottom=(sheet1_data["外資買賣超(張)"] + sheet1_data["投信買賣超(張)"]) / 1000,
    label="自營商",
    color="green"
)
plt.title("三大法人買賣超金額分佈", fontsize=16)
plt.xlabel("日期", fontsize=12)
plt.ylabel("買賣超金額 (千張)", fontsize=12)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
