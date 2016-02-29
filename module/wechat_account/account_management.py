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
import utils.date_helper as date_helper
import urllib2


class WechatAccount(object):
    def __init__(self):

        pass

    def show_accout(self, query={}):

        with MongodbUtils(config.WECHAT_DB_IP, config.WECHAT_DB_PORT, config.WECHAT_COLLECTION,
                          config.WECHAT_ACCOUNT_TABLE) as connect_db:
            _cursor = connect_db.find(query)
            res = [acct for acct in _cursor]

        return res

    def edit_account(self, acct, category="", tag=[]):
        _message = "Account name is needed"
        if acct:
            obs = dict(account=acct, category=category, tag=tag)

            with MongodbUtils(config.WECHAT_DB_IP, config.WECHAT_DB_PORT, config.WECHAT_COLLECTION,
                              config.WECHAT_ACCOUNT_TABLE) as connect_db:
                connect_db.update({"account": acct}, {"$set": obs}, upsert=True)
                _message = u"%s is updated successfully" % acct

        return _message

    def del_account(self, acct):
        _message = "Account name is needed"
        if acct:
            with MongodbUtils(config.WECHAT_DB_IP, config.WECHAT_DB_PORT, config.WECHAT_COLLECTION,
                              config.WECHAT_ACCOUNT_TABLE) as connect_db:
                connect_db.remove({"account": acct})
                _message = u"%s is removed successfully" % acct
        return _message


if __name__ == "__main__":
    wa = WechatAccount()
    # wa.edit_account("36dashuju", "tech", ["big data", "test"])
    # print wa.show_accout()
    _acct_list = [u"菜鸟教程", u"程序猿", u"大数据技术", u"大数据挖掘哪家强"]

    res = [wa.edit_account(acct, tag=["Tech"]) for acct in _acct_list]

