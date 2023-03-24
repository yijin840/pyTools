from bs4 import BeautifulSoup
from selenium import webdriver
import time
import lxml

url = "https://www.baidu.com"

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore -ssl-errors')
# 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 忽略 DevTools listening on ws://127.0.0.1... 提示
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# executable_path param is not needed if you updated PATH
browser = webdriver.Chrome(options=options, executable_path='chromedriver.exe')
browser.get(url)
time.sleep(1)
html = browser.page_source
soup = BeautifulSoup(html, features="lxml")
for li in soup.find_all("li"):
    print(li.text)
browser.quit()
 