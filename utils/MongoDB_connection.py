# -*- coding: utf-8 -*-

from pymongo import Connection
import datetime
import random
import time

db_pool={}
class MongodbUtils(object):
    def __init__(self, ip="", port=27017, collection='', table=""):
        self.table = table
        self.ip = ip
        self.port = port
        self.collection = collection
        # self.db = self.db_connection()
        # self.db_table = self.db_table_connect()

        if (ip, port) not in db_pool:
            db_pool[(ip, port)] = self.db_connection()
        elif not db_pool[(ip, port)]:
            db_pool[(ip, port)] = self.db_connection()

        self.db = db_pool[(ip, port)]
        self.db_table = self.db_table_connect()

    def __enter__(self):
        return self.db_table

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self.db.close()
        # print "exit db"
        pass

    def db_connection(self):
        db = None
        try:
            db = Connection(self.ip, self.port)
            # print "connect db", id(db)
        except Exception as e:
            print "ERRPR!"
        return db

    def db_table_connect(self):
        table_db = self.db[self.collection][self.table]
        return table_db
