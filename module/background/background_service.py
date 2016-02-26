# -*- coding: UTF-8 -*-
import sys
import requests
# from datetime import *
import time
import traceback
import numpy as np
from bs4 import BeautifulSoup
from pymongo import MongoClient
from urlparse import urlparse, parse_qs
import xml.etree.ElementTree as ET
from utils.MongoDB_connection import MongodbUtils
import config.config as config
from utils.general_tools import make_uuid
import utils.date_helper as date_helper
import urllib2
from module.crawler.wechat_crawler import WechatCrawler
from tomorrow import threads

reload(sys)
sys.setdefaultencoding("utf-8")


class BackgroundService(object):
    def __init__(self, st_dt=0, ed_dt=0, mode="update"):
        self.mode = mode

    def get_last_crawl_tsp(self, acct=""):
        if acct:
            query = {"account": acct}
        else:
            query = {}

        with MongodbUtils(config.WECHAT_DB_IP, config.WECHAT_DB_PORT, config.WECHAT_COLLECTION,
                          config.WECHAT_ACCOUNT_TABLE) as connect_db:
            _cursor = connect_db.find({"account": acct}).sort([("timestamp", 1)])
            _last = _cursor[0]
            _tsp = _last.get("timestamp", None)
        return _tsp

    # @threads(2)
    def crawl_account(self, acct):
        print "Crawling account: %s" % acct
        try:
            st = time.time()
            crawler = WechatCrawler(mode=self.mode)
            crawler.get_wechat_articles(acct)
            ed = time.time()
            status = "success"
            message = ""
        except:
            st = time.time()
            ed = time.time()
            status = "failed"
            message = traceback.format_exc()
            print message

        with MongodbUtils(config.WECHAT_DB_IP, config.WECHAT_DB_PORT, config.WECHAT_COLLECTION,
                          config.BG_SERV_CRAWL_LOG_TABLE) as connect_db:
            connect_db.insert(dict(start_date=st, end_date=ed, message=message,
                                   account=acct, status=status))

        return "Done"

    def run_wechat_crawler(self):

        # Get wechat accounts
        with MongodbUtils(config.WECHAT_DB_IP, config.WECHAT_DB_PORT, config.WECHAT_COLLECTION,
                          config.WECHAT_ACCOUNT_TABLE) as connect_db:
            _cursor = connect_db.find({})
            _acct_list = [obs.get("account") for obs in _cursor]
            print _acct_list
        # Run crawler
        res = [self.crawl_account(acct) for acct in _acct_list]

        return res


if __name__ == "__main__":
    bgs = BackgroundService(mode="init")
    bgs.run_wechat_crawler()
