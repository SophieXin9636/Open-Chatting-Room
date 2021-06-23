import requests
import demjson
from bs4 import BeautifulSoup

# 今日天氣
r = requests.get('https://www.cwb.gov.tw/Data/js/Observe/Observe_Home.js?')
time = r.text.split(" = '")[1].split("';")[0]
whether_data = r.text.split(" = '")[1].split("';")[1].split("OBS = ")[1].split(";\n")[0]
t = demjson.decode(whether_data)

print("時間", time)
for i in range(1, 14):
	if(i != 3 and i != 6 and i != 7):
		print(t[i]['CountyName']['C'] +", " + t[i]['Temperature']['C'] +"°C, " + t[i]['Weather']['C'] +", 累積雨量: " + t[i]['Rain']['C'] + " mm")
print()
# 熱門搜尋
url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=TW"
g = requests.get(url)
soup = BeautifulSoup(g.text, 'html.parser')
trend_list = soup.find_all("title")

print("熱門搜尋: ")
for i in range(1, 11):
	print("No.", i, trend_list[i].string)

# 科技資訊
