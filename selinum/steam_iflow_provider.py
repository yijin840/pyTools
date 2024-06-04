from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

url = "https://steam.iflow.work/?page_num=1&platforms=buff&games=csgo-dota2&sort_by=buy&min_price=1&max_price=5000&min_volume=2"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"


class IflowClient:
    goods_arr = [
        ["#", "饰品名称", "游戏", "日成交量", "最低售价", "最优寄售", "最优求购", "稳定求购", "近期成交", "交易平台",
         "Steam链接", "更新时间"]]

    def __init__(self, url, user_agent, time=2):
        self._url = url
        self._user_agent = user_agent
        self.time = time
        options = webdriver.ChromeOptions()
        options.add_argument('user-agent=%s' % self._user_agent)
        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore -ssl-errors')
        options.add_argument('lang=zh_CN.UTF-8')  # 设置中文
        # 忽略 DevTools listening on ws://127.0.0.1... 提示
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        # executable_path param is not needed if you updated PATH
        service = Service(executable_path='../../resouces/chromedriver.exe')
        self.driver = webdriver.Chrome(options=options, service=service)
        self.load_goods()

    def load_goods(self):
        self.driver.get(self._url)
        html = self.driver.page_source
        soup = BeautifulSoup(html, features="lxml")
        table = soup.find_all("tbody", attrs={"class": "ant-table-tbody"})
        for trx in range(1, len(table[0].find_all("tr"))):
            tr = table[0].find_all("tr")[trx]
            goods = []
            for idx in range(1, len(tr.contents)):
                content = tr.contents[idx]
                goods.append(content.text)
            self.goods_arr.append(goods)

    def start(self):
        #开始跑批
        # while True:

        pass

    def print_goods(self):
        for goods in self.goods_arr:
            for prop in goods:
                print(prop.ljust(2), end=" ")
            print("")

    def print_opt(self):
        skip_first = True
        for goods in self.goods_arr:
            if skip_first:
                skip_first = False
                continue
            for prop_idx in range(0, len(goods)):
                if prop_idx == 5 or prop_idx == 7 or prop_idx == 8:
                    continue
                print((goods[prop_idx]), end="\t")
            print("")


if __name__ == "__main__":
    iflow = IflowClient(url, user_agent)
    iflow.print_opt()
