# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class DoubanPipeline(object):
    def __init__(self, mysql_host, mysql_user, mysql_password, mysql_db):
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_db = mysql_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
            mysql_db=crawler.settings.get('MYSQL_DB')
        )

    def open_spider(self, spider):
        self.connection = pymysql.connect(host=self.mysql_host,
                                          user=self.mysql_user,
                                          password=self.mysql_password,
                                          db=self.mysql_db,
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        sql = "INSERT INTO `movie` (`title`, `director`,`writers`, `starring`,`type`, `areas`,`language`, `date`" \
              ", `run_time`,`score`, `summary`, `movie_url`) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s,%s)"
        try:
            # 执行sql语句
            self.cursor.execute(sql, (
                item['title'], item['director'], item['writers'], item['starring'], item['type'], item['areas'],
                item['language'], item['date'], item['run_time'], item['score'], item['summary'], item['movie_url']))
            # 向数据库提交
            self.connection.commit()
        except:
            # 发生错误时回滚
            self.connection.rollback()
        return item
