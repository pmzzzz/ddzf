import yaml

from modules import Sww, Qsww, Jjxxw, Qjjxxw, Rlsbj, Qrlsbj, Kjj, Customs, Qxtax, Qiyi, Dingding
from db import Mydb
import time


with open('config.yml', 'r') as c:
    conf = yaml.load(c)['dingding']
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

while True:
    try:
        time.sleep(1)
        time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
        if time_now == '21:00:00':
            mysql = Mydb()
            log.test('开始爬了')
            for i in items:
                try:
                    datas = i.get_html().get_data_all().datas
                    mysql.insert(datas=datas)
                    # print('插入完成' + str(len(datas)))
                except Exception as e:
                    log.test('{}数据库爬的时候错啦'.format(i.source)+e.__str__())
            mysql.end()
            log.test('爬完了')
    except Exception as e:
        log.test('数据库错啦'+str(e))
        continue
