# -*- coding: UTF-8 -*-
import datetime

import requests
import selenium.common.exceptions
from bs4 import BeautifulSoup
import json
from utils.utils import get_url, get_html, get_html_1, get_dd_url
import time


class Dingding:
    def __init__(self, url, secret):
        self.url = url
        self.secret = secret

    def send_message(self, message):
        url = get_dd_url(self.url, self.secret)
        headers = {'Content-Type': 'application/json',
                   'charset': 'utf-8'}
        x = requests.post(url=url, data=json.dumps(message), headers=headers)
        print(x.text)

    def test(self, text="这是一个消息发送测试^_^"):
        message = {
            "at": {
                "atMobiles": [],
                "atUserIds": [],
                "isAtAll": False
            },
            "text": {
                "content": text
            },
            "msgtype": "text"
        }
        self.send_message(message)


class BigSpider:
    def __init__(self, url, source):
        self.url = url
        self.source = source
        self.html = ''
        self.datas = []  # 标题、链接、显示、来源、发布时间、爬取时间、板块

    def get_html(self):
        """
        获得网页源代码
        :return:
        """
        url = self.url
        try:
            html = get_html_1(url)
        except selenium.common.exceptions.TimeoutException:
            try:
                html = get_html(url)
            except:
                pass
        self.html = html
        return self


# 重庆市商委委员会主页
class Sww(BigSpider):
    def __init__(self, url='http://sww.cq.gov.cn', source='重庆市商委委员会') -> object:
        super(Sww, self).__init__(url, source)

    def get_data_all(self):
        html = self.html
        soup = BeautifulSoup(html, 'html.parser')
        # 国务院信息cqjrcq
        uls = soup.find_all('ul', attrs={'class': "tab-item"})
        tabs = ['国务院信息', '今日重庆', '部门动态', '通知公告', '行业信息', '履职依据', '政策解读']
        datas = []
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        for ul, tab in zip(uls, tabs):
            a = ul.find_all('a')
            span = ul.find_all('span')
            for aa, ss in zip(a, span):
                data = {'标题': aa.attrs['title'], '链接': get_url(self.url, aa.attrs['href']), '显示': aa.text,
                        '来源': self.source, '发布时间': ss.text, '爬取时间': now, '板块': tab}
                datas.append(data)
        self.datas = datas
        return self

    def show_datas(self):
        print(self.datas)

    def save_data(self):
        pass

    def search(self, kw):
        pass


# 渝北区商委委员会主页
class Qsww(BigSpider):
    def __init__(self, url='http://www.ybq.gov.cn/bm/qsww', source='渝北区商委'):
        super(Qsww, self).__init__(url, source)

    def get_data(self):
        url = self.url
        r = requests.get(url=url)
        html = r.content.decode('utf8')
        soup = BeautifulSoup(html, 'html.parser')
        ul = soup.find_all('ul', class_="tab-item")[0]
        a = ul.find_all('a')
        span = ul.find_all('span')
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        datas = []
        for aa, ss in zip(a, span):
            data = {'标题': aa.attrs['title'], '链接': self.url + aa.attrs['href'][1:], '显示': aa.text,
                    '来源': '渝北区商委委员会', '发布时间': ss.text, '爬取时间': now}
            datas.append(data)
        self.datas = datas
        return self

    def get_data_all(self):
        html = self.html
        soup = BeautifulSoup(html, 'html.parser')
        uls = soup.find_all('ul', attrs={'class': "tab-item"})
        tabs = ['动态要闻', '履职依据']
        datas = []
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        for ul, tab in zip(uls, tabs):
            a = ul.find_all('a')
            span = ul.find_all('span')
            for aa, ss in zip(a, span):
                data = {'标题': aa.attrs['title'], '链接': get_url(self.url, aa.attrs['href']), '显示': aa.text,
                        '来源': self.source, '发布时间': ss.text, '爬取时间': now, '板块': tab}
                datas.append(data)
        self.datas = datas
        return self

    def show_datas(self):
        print(self.datas)

    def save_data(self):
        pass

    def search(self, kw):
        pass


# 重庆市经济和信息化委员会主页
class Jjxxw(BigSpider):
    def __init__(self, url='https://jjxxw.cq.gov.cn', source='重庆市经济和信息化委员会'):
        super(Jjxxw, self).__init__(url, source)

    def get_data(self):
        url = self.url
        r = requests.get(url=url, verify=False)
        html = r.content.decode('utf8')
        soup = BeautifulSoup(html, 'html.parser')
        ul = soup.find_all('ul', class_="tab-item")[2]
        a = ul.find_all('a')
        span = ul.find_all('span')
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

        datas = []
        for aa, ss in zip(a, span):
            data = {'标题': aa.attrs['title'], '链接': self.url + aa.attrs['href'][1:], '显示': aa.text,
                    '来源': '重庆市经济和信息化委员会', '发布时间': ss.text, '爬取时间': now}
            datas.append(data)
        self.datas = datas
        return self

    def get_data_all(self):
        html = self.html
        soup = BeautifulSoup(html, 'html.parser')
        # 国务院信息cqjrcq
        uls = soup.find_all('ul', attrs={'class': "tab-item"})
        tabs = ['国务院信息', '今日重庆', '信经动态', '新闻发布', '政策文件', '公示公告']
        datas = []
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        for ul, tab in zip(uls, tabs):
            a = ul.find_all('a')
            span = ul.find_all('span')
            for aa, ss in zip(a, span):
                data = {'标题': aa.attrs['title'], '链接': get_url(self.url, aa.attrs['href']), '显示': aa.text,
                        '来源': self.source, '发布时间': ss.text, '爬取时间': now, '板块': tab}
                datas.append(data)
        self.datas = datas
        return self

    def show_datas(self):
        print(self.datas)

    def save_data(self):
        pass

    def search(self, kw):
        pass


# 渝北区经济和信息化委员会
class Qjjxxw(BigSpider):
    def __init__(self, url='http://www.ybq.gov.cn/bm/qjjxxw', source='渝北区经济和信息化委员会'):
        super(Qjjxxw, self).__init__(url, source)

    def get_data(self):
        url = self.url
        r = requests.get(url=url, verify=False)
        html = r.content.decode('utf8')
        soup = BeautifulSoup(html, 'html.parser')
        ul = soup.find_all('ul', class_="tab-item")[0]
        a = ul.find_all('a')
        span = ul.find_all('span')
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

        datas = []
        for aa, ss in zip(a, span):
            data = {'标题': aa.attrs['title'], '链接': self.url + aa.attrs['href'][1:], '显示': aa.text,
                    '来源': '渝北区经济和信息化委员会', '发布时间': ss.text, '爬取时间': now}
            datas.append(data)
        self.datas = datas
        return self

    def get_data_all(self):
        html = self.html
        soup = BeautifulSoup(html, 'html.parser')
        uls = soup.find_all('ul', attrs={'class': "tab-item"})
        tabs = ['动态要闻', '履职依据']
        datas = []
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        for ul, tab in zip(uls, tabs):
            a = ul.find_all('a')
            span = ul.find_all('span')
            for aa, ss in zip(a, span):
                data = {'标题': aa.attrs['title'], '链接': get_url(self.url, aa.attrs['href']), '显示': aa.text,
                        '来源': self.source, '发布时间': ss.text, '爬取时间': now, '板块': tab}
                datas.append(data)
        self.datas = datas
        return self

    def show_datas(self):
        print(self.datas)

    def save_data(self):
        pass

    def search(self, kw):
        pass


# 重庆市人力资源和社会保障局主页
class Rlsbj(BigSpider):
    def __init__(self, url='http://rlsbj.cq.gov.cn', source='重庆市人力资源和社会保障局'):
        super(Rlsbj, self).__init__(url, source)

    def get_data(self):
        url = self.url
        r = requests.get(url=url)
        html = r.content.decode('utf8')
        soup = BeautifulSoup(html, 'html.parser')
        ul = soup.find_all('ul', class_="tab-item")[2]
        a = ul.find_all('a')
        span = ul.find_all('span')
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

        datas = []
        for aa, ss in zip(a, span):
            data = {'标题': aa.attrs['title'], '链接': self.url + aa.attrs['href'][1:], '显示': aa.text,
                    '来源': '重庆市人力资源和社会保障局', '发布时间': ss.text, '爬取时间': now}
            datas.append(data)
        self.datas = datas
        return self

    def get_data_all(self):
        html = self.html
        soup = BeautifulSoup(html, 'html.parser')
        # 国务院信息cqjrcq
        uls = soup.find_all('ul', attrs={'class': "tab-item"})
        tabs = ['国务院信息', '今日重庆', '通知公告', '工作动态', '政策解读', '事业单位公开招聘', '人事考试', '专技人才', '新闻头条', '公示信息', '社会保险', '人才社会服务']
        datas = []
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        for ul, tab in zip(uls, tabs):
            a = ul.find_all('a')
            span = ul.find_all('span')
            for aa, ss in zip(a, span):
                data = {'标题': aa.attrs['title'], '链接': get_url(self.url, aa.attrs['href']), '显示': aa.text,
                        '来源': self.source, '发布时间': ss.text, '爬取时间': now, '板块': tab}
                datas.append(data)
        self.datas = datas
        return self

    def show_datas(self):
        print(self.datas)

    def save_data(self):
        pass

    def search(self, kw):
        pass


# 渝北区人力资源和社会保障局主页
class Qrlsbj(Qsww):
    def __init__(self, url='http://www.ybq.gov.cn/bm/qrlsbj', source='渝北区人力资源和社会保障局'):
        super(Qrlsbj, self).__init__(url, source)

    def get_data(self):
        url = self.url
        r = requests.get(url=url)
        html = r.content.decode('utf8')
        soup = BeautifulSoup(html, 'html.parser')
        ul = soup.find_all('ul', class_="tab-item")[0]
        a = ul.find_all('a')
        span = ul.find_all('span')
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        datas = []
        for aa, ss in zip(a, span):
            data = {'标题': aa.attrs['title'], '链接': self.url + aa.attrs['href'][1:], '显示': aa.text,
                    '来源': '渝北区人力资源和社会保障局', '发布时间': ss.text, '爬取时间': now}
            datas.append(data)
        self.datas = datas
        return self

    def show_datas(self):
        print(self.datas)

    def save_data(self):
        pass

    def search(self, kw):
        pass


# 重庆市科学技术局
class Kjj(BigSpider):
    def __init__(self, url='http://kjj.cq.gov.cn', source='重庆市科学技术局'):
        super(Kjj, self).__init__(url, source)

    def get_data(self):
        url = self.url
        r = requests.get(url=url)
        html = r.content.decode('utf8')
        soup = BeautifulSoup(html, 'html.parser')
        ul = soup.find_all('ul', class_="tab-item")[2]
        a = ul.find_all('a')
        span = ul.find_all('span')
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

        datas = []
        for aa, ss in zip(a, span):
            data = {'标题': aa.attrs['title'], '链接': self.url + aa.attrs['href'][1:], '显示': aa.text,
                    '来源': '重庆市科学技术局', '发布时间': ss.text, '爬取时间': now}
            datas.append(data)
        self.datas = datas
        return self

    def get_data_all(self):
        html = self.html
        soup = BeautifulSoup(html, 'html.parser')
        uls = soup.find_all('ul', attrs={'class': "tab-item"})
        tabs = ['工作动态', '科技动态', '通知公告', '国务院信息', '今日重庆', '国务院文件', '市政府文件', '履职依据', '科技政策解读', '政协提案办理情况公开',
                '人大代表建议办理情况公开', '预算/决算']
        datas = []
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        for ul, tab in zip(uls, tabs):
            a = ul.find_all('a')
            span = ul.find_all('span')
            for aa, ss in zip(a, span):
                data = {'标题': aa.attrs['title'], '链接': get_url(self.url, aa.attrs['href']), '显示': aa.text,
                        '来源': self.source, '发布时间': ss.text, '爬取时间': now, '板块': tab}
                datas.append(data)
        self.datas = datas
        return self

    def show_datas(self):
        print(self.datas)

    def save_data(self):
        pass

    def search(self, kw):
        pass


# 重庆海关
class Customs(BigSpider):
    def __init__(self, url='http://chongqing.customs.gov.cn', source='重庆海关'):
        super(Customs, self).__init__(url, source)

    def get_data_all(self):
        html = self.html
        soup = BeautifulSoup(html, 'html.parser')

        uls = soup.find_all('ul', attrs={'class': 'customs-news-list'}
                            ) + soup.find_all('ul', attrs={'class': "zwgk_news_list"})

        tabs = ['本关动态', '图片新闻', '本关公告', '政策解读', '政府采购', '拍卖信息']
        datas = []
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        for ul, tab in zip(uls, tabs):
            a = ul.find_all('a')
            span = ul.find_all('span')
            for aa, ss in zip(a, span):
                data = {'标题': aa.attrs['title'], '链接': get_url(self.url, aa.attrs['href']), '显示': aa.text,
                        '来源': self.source, '发布时间': ss.text, '爬取时间': now, '板块': tab}
                datas.append(data)
        self.datas = datas
        return self

    def show_datas(self):
        print(self.datas)

    def save_data(self):
        pass

    def search(self, kw):
        pass


# 重庆税务局
class Qxtax(BigSpider):
    def __init__(self, url='http://chongqing.chinatax.gov.cn/qxtax/yb', source='重庆税务局'):
        super(Qxtax, self).__init__(url, source)

    def get_data_all(self):
        html = self.html
        soup = BeautifulSoup(html, 'html.parser')
        uls = soup.find_all('ul')[3:5]
        tabs = ['工作动态', '通知公告']
        datas = []
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        for ul, tab in zip(uls, tabs):
            a = ul.find_all('a')
            dt = ul.find_all('dt')
            for aa, dd in zip(a, dt):
                data = {'标题': aa.text, '链接': get_url(self.url, aa.attrs['href']), '显示': aa.text,
                        '来源': self.source, '发布时间': str(datetime.datetime.now().year) + "-" + dd.text, '爬取时间': now,
                        '板块': tab}
                datas.append(data)
        self.datas = datas
        return self

    def show_datas(self):
        print(self.datas)

    def save_data(self):
        pass

    def search(self, kw):
        pass


# 七一网
class Qiyi(BigSpider):
    def __init__(self, url='https://www.12371.gov.cn', source='七一网'):
        super(Qiyi, self).__init__(url, source)

    def get_data_all(self):
        html = self.html
        soup = BeautifulSoup(html, 'html.parser')
        ul = soup.find_all('ul', class_="topicList")[0]
        a = ul.find_all('a')
        span = ul.find_all('span', class_="date")
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

        datas = []
        for aa, ss in zip(a, span):
            data = {'标题': aa.attrs['title'], '链接': get_url(self.url, aa.attrs['href']), '显示': aa.text,
                    '来源': self.source, '发布时间': str(datetime.datetime.now().year) + "-" + ss.text, '爬取时间': now,
                    '板块': '热点新闻'}
            datas.append(data)
        self.datas = datas
        return self

    def show_datas(self):
        print(self.datas)

    def save_data(self):
        pass

    def search(self, kw):
        pass


# 别人
# https://oapi.dingtalk.com/robot/send?access_token=55a631bf9d073d08d646782aab946611db5324bcc12421c1320958e14dce8713
# SECd3a19efd5a62c0b033ca5a1163947010edca0c6a6a072afa7790d27c8733e412


if __name__ == '__main__':
    sww = Sww()
    qsww = Qsww()
    jjxxw = Jjxxw()
    qjjxxw = Qjjxxw()
    rlsbj = Rlsbj()
    qrlsbj = Qrlsbj()
    kjj = Kjj()
    customs = Customs()
    qxtaxt = Qxtax()
    qiyi = Qiyi()
    items = [sww, qsww, jjxxw, qjjxxw, rlsbj, qrlsbj, kjj, customs, qxtaxt, qiyi]

    print(qiyi.get_html().get_data_all().datas)
