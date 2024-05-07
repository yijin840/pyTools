import requests

uu = "https://steam.iflow.work/zh-CN?page_num=1&platforms=buff&games=csgo&sort_by=buy&min_price=10&max_price=5000&min_volume=2"
resp = requests.get(uu)

print(resp)