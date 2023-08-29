# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class WebCrawler:
    def get(self, url, proxy=None, sleep=0, headers=None):
        opt = Options()
        opt.add_argument("--headless")
        opt.add_argument("--ignore-certificate-errors")
        opt.add_argument("--ignore -ssl-errors")
        opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument("start-maximized")
        opt.add_argument("user-agent=%s" % headers["User-Agent"])
        opt.add_argument("--disable-blink-features=AutomationControlled")
        # 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
        opt.add_experimental_option("excludeSwitches", ["enable-automation"])
        # 忽略 DevTools listening on ws://127.0.0.1... 提示
        opt.add_experimental_option("excludeSwitches", ["enable-logging"])
        # Change the link below for adding proxy
        if proxy != None:
            opt.add_argument("--proxy-server=%s" % proxy)
        # opt.page_load_strategy = 'eager'
        # executable_path param is not needed if you updated PATH
        driver = webdriver.Edge(options=opt)
        driver.get(url)
        # 等待时间
        driver.implicitly_wait(sleep)
        return driver.page_source

    # 过 cloudfare 安全认证 （未实现）
    def passCloudFare(driver):
        pass

    #登录 (未完全实现)
    def login(self, driver, sleep, email, pwd):
         # 输入用户名和密码
        username = driver.find_element(By.NAME, "session[email]")
        password = driver.find_element(By.NAME, "session[password]")
        username.send_keys(email)
        password.send_keys(pwd)
        driver.find_element(By.ID, "login-btn").click()
        response = driver.execute_script("return document.body.textContent;")
        driver.quit()
        return response
