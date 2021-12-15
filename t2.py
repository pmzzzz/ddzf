# -*- coding: UTF-8 -*-
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options

display = Display(visible=0, size=(800,600))
display.start()

options = Options()
options.add_argument("--no-sandbox")
# 隐藏 正在受到自动软件的控制 这几个字
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path='/opt/google/chrome/chromedriver') #Chrome驱动的位置，此学习记录>中安装到了Chrome程序根目录，该路径为绝对路径

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        })
driver.get('http://sww.cq.gov.cn')
driver.implicitly_wait(5)
import time
time.sleep(5)
from bs4 import BeautifulSoup
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
print(soup)
driver.quit()
display.stop()
