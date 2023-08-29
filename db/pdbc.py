#!/usr/bin/python3

import pymysql


class pdbc:
    conn = None
    cursor = None

    def __init__(self, host, user, password, database):
        self.conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.conn.cursor()
        self.conn.set_charset("utf8")

    def execute(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def insert(self, sql):
        self.execute(self, sql)

    def queryOne(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    def queryAll(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def update(self, sql):
         self.execute(self, sql)

    def close(self):
        self.conn.close()
