import pandas as pd
import bs4
import requests
# 放入類股的網頁
url = "https://goodinfo.tw/tw/StockList.asp?MARKET_CAT=%E5%85%A8%E9%83%A8&INDUSTRY_CAT=%E8%BE%B2%E6%A5%AD%E7%A7%91%E6%8A%80%E6%A5%AD&SHEET=%E5%AD%A3%E8%B3%87%E7%94%A2%E7%8B%80%E6%B3%81&SHEET2=%E8%B3%87%E7%94%A2%E8%B2%A0%E5%82%B5%E9%87%91%E9%A1%8D&RPT_TIME=%E6%9C%80%E6%96%B0%E8%B3%87%E6%96%99"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
           'Cookie': "CLIENT%5FID=20240125133737886%5F203%2E64%2E105%2E149; _ga=GA1.1.613331571.1706161060; IS_TOUCH_DEVICE=F; SCREEN_SIZE=WIDTH=1280&HEIGHT=720; _cc_id=54fadce9bf9e2cbe2cd5bbb606d79d58; TW_STOCK_BROWSE_LIST=4919%7C2330%7C6235%7C3515%7C2722%7C3231%7C2453%7C00919%7C0056%7C1101%7C4763%7C5284%7C2376%7C3035%7C2363%7C3056%7C6139%7C0050%7C6452%7C6451; panoramaId_expiry=1733571222973; panoramaId=b89a34595c38d175d56cd35698e016d539382ef9a84cbf50c0d3fa809767659f; panoramaIdType=panoIndiv; __gads=ID=04f6f49a4e45b518:T=1706880828:RT=1733140786:S=ALNI_MbwLOCe1Tu6qqdvN4cCBE6PJPaQew; __gpi=UID=00000cf6f3f146ef:T=1706880828:RT=1733140786:S=ALNI_MYYw-nwv7LGqawQx095RgLKmLWeog; __eoi=ID=77a830dee7404b71:T=1732256788:RT=1733140786:S=AA-AfjZWiXt6J67nSTb1bVscq5XV; cto_bundle=ikWpSF9LUTZ1NVI3YlgyNkR6bnBGcVRQRWY3akZrcU1YJTJGTEhPY1ZBUnBBazFvZUU1ckR2amhVODg2ajVPWGdFVm5LaTRQMXNUd1UlMkZPeVBtNDhNTHRIb21YaGprczE0WW5KJTJCaHBXNFhOQnJkZ1JKOGRWZ0hmcEpqUUg1ZEFQQkNjZzRxcGwlMkJpb0xTOSUyRnR1RXp4N3VTUWU1T05PME02SlozJTJCekg0Wk9qamdjMXJmejFUeHA5NDhXQ2ZqV3R0akElMkZJQ3lWcmMwYXhRRVYxQUdYVmp2SlRURDI2TlElM0QlM0Q; cto_bidid=c5ou6l9FbyUyQlpXRnNUaERiSjRuMWNTUkdIUUpaUU1WWW9iOHE2RERscGFwTElzNnRKTUM1ejB2QzY4TTlDMGVhOHllbk5ycjJiWGV3Z1ZuOSUyQmd4UnFOSk5GZDVTa29odXlvQWVqS3lwa2F0WjNPeVklM0Q; _ga_0LP5MLQS7E=GS1.1.1733140030.38.1.1733140798.44.0.0; FCNEC=%5B%5B%22AKsRol_UvQ5T4DPmJdVT42cWMlLYS9vaskc8PgibDH-iOWVP3eTLc_j3QwfDUik-T5L3GfRGz0SzrZBU1yijMqLcSaWgd22PmB25nJmk76riPnewX7hJZgPZs_6xZWYUqaoUdDn9N12wwhT80px8JDpEyADT1SUahw%3D%3D%22%5D%5D; cto_bundle=mClHtV9LUTZ1NVI3YlgyNkR6bnBGcVRQRWYzUVo2elJaT1JEZUZVU2VRSjBVclBWeVNPZkRnQkQ3eGIlMkZhNFl0VkthMnk4bWZQOGxWTDBVenF5UGNxOFpnRkJDV2p3a21YMHN2TVA5WldSSEFGYldiazNzclpNZSUyQjlhMEVleFZKZThYR0NJV0RtNUN0c25UJTJGNTF3dmJ6b1NkcEFsTk1sZEJ5ZkN0NWQ0QzNZMmwwSGZFJTJGbERVM0ZjdTJ4VllNR2psU2IwbjhhZmNsbyUyQlpCZlVpd0JSQnpMVkVXUSUzRCUzRA"}
res = requests.get(url, headers=headers)
res.encoding = "utf-8"
# %%

soup = bs4.BeautifulSoup(res.text, "lxml")
data = soup.select_one("#tblStockList")
# %%
# 用.prettify()將data整理得更好且用read_html來找到表格
df = pd.read_html(data.prettify())
# 看有幾個表格
len(df)
# 第[1]表格為我們的目標。
dfs = df[0]
# 整理表格的標頭
# dfs.columns = dfs.columns.get_level_values(16)
# del
# Filter to keep only rows where '代號' contains numeric values
dfs = dfs[dfs['代號'].apply(lambda x: str(x).isdigit())]
# Reset the index if needed
dfs.reset_index(drop=True, inplace=True)
# 顯示頭幾筆資料
dfs.head()
dfs.to_excel("農業科技業.xlsx", index=False)
