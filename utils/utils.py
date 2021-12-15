# -*- coding: UTF-8 -*-
import hmac
import hashlib
import urllib
import base64
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display


def get_dd_url(url=None, secret=None):
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url1 = url + '&timestamp=' + timestamp + '&sign=' + sign
    return url1


def form_message(datas: list, source):
    source = source
    links = '### 【{}】'.format(source)
    if datas:
        titles = [i['标题'] for i in datas]
        hrefs = [i['链接'] for i in datas]
        tabs = [i['板块'] for i in datas]
        i = 1
        for name, href, tab in zip(titles, hrefs, tabs):
            name = '{}、{}[{}]'.format(i, name, tab)
            i += 1
            # one = '- [{}]({})\n'.format(name, href)
            one = '\n{}\n{}\n\n'.format(name, href)
            one = '\n{}\n[{}]({})\n\n'.format(name, '查看详情', href)
            links += one
    else:
        return links + '\n- 今日无数据'
    return links


def get_message(links):
    send_data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "今日公告",
            "text": "{}".format(links)
        },
        "at": {
            "isAtAll": True
        }
    }
    return send_data





def get_html_1(url):
    display = Display(visible=False, size=(800, 600))
    display.start()

    options = Options()
    options.add_argument("--no-sandbox")
    # 隐藏 正在受到自动软件的控制 这几个字
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options,
                              executable_path='/opt/google/chrome/chromedriver')  # Chrome驱动的位置，此学习记录>中安装到了Chrome程序根目录，该路径为绝对路径

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    driver.set_page_load_timeout(20)
    driver.get(url)
    driver.implicitly_wait(5)
    # html = driver.page_source
    time.sleep(5)
    # driver.close()
    html = driver.page_source
    driver.quit()
    display.stop()
    return html


def get_html(url):
    options = Options()
    display = Display(visible=False, size=(1200, 800))
    display.start()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")

    # 隐藏 正在受到自动软件的控制 这几个字
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options, executable_path='/opt/google/chrome/chromedriver')
    driver.set_page_load_timeout(20)
    # 修改 webdriver 值
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    print('开始获取页面')
    driver.implicitly_wait(5)

    driver.get(url)

    time.sleep(5)
    # driver.find_element_by_class_name('clearfix')
    html = driver.page_source
    driver.quit()
    display.stop()
    return html


def get_url(base_url, url):
    if url[:4] == 'http':
        return url
    if url[:5] == '../..':
        return '/'.join(base_url.split('/')[:-2]) + url[5:]
    elif url[:3] == '../':
        return '/'.join(base_url.split('/')[:-1]) + url[2:]
    elif url[:1] == '.':
        return base_url + url[1:]
    else:
        return base_url + '/' + url


def filter_by_date(datas: list, dates: list):
    r = list(filter(lambda x: x['发布时间'] in dates, datas))
    return r


# 政策申报、补贴、培训会

def check(t: str, ws: list):
    f = False
    for w in ws:
        if w in t:
            f = True
            break
    print(f)
    return f


def filter_by_kw(datas: list, kws: list):
    # ws = list(''.join(kws))
    ws = kws
    print(ws)
    r = []
    for data in datas:
        if check(data['标题'], ws):
            r.append(data)
            print(data)
    return r


if __name__ == '__main__':
    url = 'http://www.ybq.gov.cn/bm/qsww'
    # html = get_html(url)
    # soup = BeautifulSoup(html, 'html.parser')
    # lis = soup.find_all('li',attrs={"class":"clearfix"})
    # print(lis)
    datas = [{'发布时间': '2021-06-22'}, {'发布时间': '2021-06-21'}]

    print(filter_by_date(datas, [str(datetime.date.today())]))
    print(get_url(url, './zwgk_263/zfxxgkml/zcwj/xzgfxwj/zfgfxwj/202011/t20201123_8487503.html'))
    print(type(datetime.date.today()))
