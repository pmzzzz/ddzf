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
    log = Dingding(
        url=conf['log']['url'],
        secret=conf['log']['secret']
    )

    bb = items
    for i in bb:
        i.get_html().get_data_all()
        datas = i.datas
        source = i.source
        r = filter_by_date(datas, [str(datetime.date.today()),
                                   str(datetime.date.today() + datetime.timedelta(-1))])
        r = filter_by_kw(r, '政策、补贴、职业、技能'.split('、'))
        links = form_message(r, source)
        message = get_message(links)
        if r:
            log.send_message(message)
        time.sleep(1)
