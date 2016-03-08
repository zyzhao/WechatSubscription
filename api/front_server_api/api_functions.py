# -*- coding: UTF-8 -*-
import sys
import requests
# from datetime import *
import time
import numpy as np
from bs4 import BeautifulSoup
from pymongo import MongoClient
from urlparse import urlparse, parse_qs
import xml.etree.ElementTree as ET
from utils.MongoDB_connection import MongodbUtils
import config.config as config
from utils.general_tools import make_uuid
from utils.decorator import try_except, simulate_human, try_except_parse
import utils.date_helper as date_helper
import urllib2
import cookielib
from utils.log import LOG
import traceback
from module.crawler.web_browser import WebBrowser
from module.crawler.wechat_crawler import WechatCrawler

def article_summary_list(query={}, pn=1, ps=10):
    res = []
    if pn > 0 and ps > 0:
        with MongodbUtils(config.WECHAT_DB_IP, config.WECHAT_DB_PORT, config.WECHAT_COLLECTION,
                                  config.WECHAT_ARTICLE_SUMMARY_TABLE) as connect_db:
            _cursor = connect_db.find(query).sort([("release_date", -1)]).skip(ps*(pn-1)).limit(ps)
        res = [item for item in _cursor]

    return {"article_list": res}


def account_list(query={}, pn=1, ps=10):
    res = []
    # if pn > 0 and ps > 0:
    with MongodbUtils(config.WECHAT_DB_IP, config.WECHAT_DB_PORT, config.WECHAT_COLLECTION,
                              config.WECHAT_ACCOUNT_TABLE) as connect_db:
        _cursor = connect_db.find(query)
    res = [item for item in _cursor]
    return {"account_list": res}


def add_account(keywords=[]):
    if keywords:
        for k in keywords:
            res = WechatCrawler().act_search_account(k)

    return {"status": "Done"}



if __name__ == "__main__":
    # print article_summary_list()
    # print account_list()
    add_account(u"优秀网页设计")
