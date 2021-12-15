# -*- coding: UTF-8 -*-

import yaml
from modules import *
from utils.utils import filter_by_kw, filter_by_date, form_message, get_message

with open('config.yml', 'r') as c:
    conf = yaml.load(c)['dingding']

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

    yewu = Dingding(
        url=conf['yewu']['url'],
        secret=conf['yewu']['secret']
    )
    log = Dingding(
        url=conf['log']['url'],
        secret=conf['log']['secret']
    )
    while True:
        try:
            time.sleep(1)
            time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
            if time_now == conf['send']['time']:  # 此处设置每天定时的时间
                print('开始爬取')
                # 爬取数据
                bb = items
                try:
                    for i in bb:
                        i.get_html().get_data_all()
                    log.test('以下是过滤后数据：')
                    yewu.test('以下是过滤后数据:')
                    time.sleep(2)
                except:
                    pass
                for i in bb:
                    datas = i.datas
                    source = i.source
                    r = filter_by_date(datas, [str(datetime.date.today()),
                                               str(datetime.date.today() + datetime.timedelta(-1))])
                    r = filter_by_kw(r, '政策、补贴、职业、技能'.split('、'))
                    links = form_message(r, source)
                    message = get_message(links)
                    if r:
                        log.send_message(message)
                        yewu.send_message(message)
                    time.sleep(1)
        except:
            log.send_message('错误，请检查程序')
            continue
