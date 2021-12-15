import pymysql
import yaml

with open('config.yml', 'r') as c:
    conf = yaml.load(c)['mysql']


class Mydb:
    def __init__(self):

        self.host = conf['host']
        self.user = conf['user']
        self.passwd = conf['passwd']
        self.db = conf['dbname']
        self.port = conf['port']
        self.connection = pymysql.connect(host=self.host, password=self.passwd, database=self.db, port=self.port)
        self.cursor = self.connection.cursor()

    def end(self):
        self.cursor.close()
        self.connection.close()

    # 标题、链接、显示、来源、发布时间、爬取时间、板块
    def insert(self, datas: list):
        values = [(i['标题'], i['链接'], i['显示'], i['来源'], i['发布时间'], i['爬取时间'], i['板块']) for i in datas]
        try:
            self.cursor.executemany(
                'replace into links (title,link,display,pub_dep,pub_time,scrap_time,tab) values (%s,%s,'
                '%s,%s,%s,%s,%s) ', values)
            self.connection.commit()
        except Exception as err:
            print(err)

    def close(self):
        self.cursor.close()
        self.connection.close()
