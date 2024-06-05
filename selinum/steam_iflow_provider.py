from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import requests
url = "https://steam.iflow.work/?page_num=1&platforms=buff&games=csgo-dota2&sort_by=buy&min_price=1&max_price=5000&min_volume=2"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"

class IflowClient:
    goods_arr = [
        ["#", "饰品名称", "游戏", "日成交量", "最低售价", "最优寄售", "最优求购", "稳定求购", "近期成交", "交易平台",
         "Steam链接", "更新时间"]]
    goods = []
    def __init__(self, url, user_agent, driver_path, time=2):
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
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(options=options, service=service)
        self.driver.get(self._url)
        self.load_goods()

    def load_goods(self):
        try:
            time.sleep(5)
            html = self.driver.page_source
            soup = BeautifulSoup(html, features="lxml")
            table = soup.find_all("tbody", attrs={"class": "ant-table-tbody"})
            for trx in range(1, len(table[0].find_all("tr"))):
                tr = table[0].find_all("tr")[trx]
                buff_url = self.get_btn_link(trx)
                self.goods = []
                for idx in range(1, len(tr.contents)):
                    content = tr.contents[idx]
                    self.goods.append(content.text)
                self.goods.append(buff_url)
                # self.goods_arr.append(goods)
                return
        except:
            print("load_goods error...")
        
    def start(self):
        while True:
            if float(self.goods[6]) < 0.70:
                print(self.goods)
                self.push_message()
            time.sleep(10)
            self.load_goods()
    
    def push_message(self):
        if(lastGoodsName == self.goods[1]):
            return
        lastGoodsName = self.goods[1]
        desp = '\n'.join(f'* {item}' for item in self.goods)
        data = {
            'title': f"{self.goods[1]}",
            'desp': desp
        }
        url=f"https://sctapi.ftqq.com/%s.send"
        resp = requests.post(url, data=data)
        print(resp.content.decode("utf-8"))

    def get_btn_link(self, idx):
        # 使用 JavaScript 获取按钮元素并点击
        button_xpath = f"/html/body/main/section/div[2]/div/div/div/div/div/div/div[2]/table/tbody/tr[{idx+1}]/td[11]/button"
        # print(button_xpath)
        button_script = f"""
        var button = document.evaluate('{button_xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        button.click();
        console.log(button);
        """
        # 执行 JavaScript 代码
        self.driver.execute_script(button_script)
        # 等待一段时间确保页面加载完成
        time.sleep(5)
        current_window_handle = self.driver.current_window_handle
        # 获取所有窗口句柄
        all_window_handles = self.driver.window_handles
        old_window_handle = current_window_handle
        # 切换到新打开的标签页
        new_window_handle = [handle for handle in all_window_handles if handle != current_window_handle][0]
        self.driver.switch_to.window(new_window_handle)
        current_url = self.driver.current_url
        #切换回来        
        # print(current_url)
        self.driver.switch_to.window(old_window_handle)
        return current_url

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
    iflow = IflowClient(url, user_agent, "pyTools/selinum/chromedriver")
    iflow.start()
