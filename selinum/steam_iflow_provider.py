from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import lxml
from selenium.webdriver.common.proxy import *
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = "https://steam.iflow.work/?page_num=1&platforms=buff&games=csgo-dota2&sort_by=buy&min_price=1&max_price=5000&min_volume=2"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"

options = webdriver.ChromeOptions()
options.add_argument('user-agent=%s'%user_agent)
options.add_argument('--headless')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore -ssl-errors')
options.add_argument('lang=zh_CN.UTF-8') # 设置中文
# 忽略 DevTools listening on ws://127.0.0.1... 提示
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
# executable_path param is not needed if you updated PATH
service = Service(executable_path='/Users/onchain/wys/pytools/pyTools/selinum/chromedriver')
driver = webdriver.Chrome(options=options, service=service)
driver.get(url)
time.sleep(2)
html = driver.page_source
soup = BeautifulSoup(html, features="lxml")
table = soup.find_all("tbody",attrs={"class":"ant-table-tbody"})

goods = [str]
goods_arr = [goods]
for trx in range(0, len(table[0].find_all("tr"))):
    tr = table[0].find_all("tr")[trx]
    element_xpath = '/html/body/main/section/div[2]/div/div/div/div/div/div/div[2]/table/tbody/tr[%s]/td[11]/button/span'%(trx+2)
    element = driver.find_element(By.PARTIAL_LINK_TEXT, "i")
    
    print(element.get_property("innerHTML"))
    element.click()
    driver.execute_script("arguments[0].click()", element)
    # print(i.get_property("innerHTML"))
    print(driver.current_url)

    # print(element[0].get_property("innerHTML"))
    # element[0].click()
    # print(driver.current_url)
    break
    # print(element.text)
    # print(len(tr.contents))
    for content in tr.contents:
        goods.append(content.text)
    goods_arr.append(goods)
# print(table)

# # print(goods_arr)
driver.quit()
 
