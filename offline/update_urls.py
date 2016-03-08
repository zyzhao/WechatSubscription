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
from module.crawler.baidu_crawler import BaiduCrawler

with MongodbUtils(config.WECHAT_DB_IP, config.WECHAT_DB_PORT, config.WECHAT_COLLECTION,
                              config.WECHAT_ARTICLE_SUMMARY_TABLE) as connect_db:
    _cursor = connect_db.find()
    for item in _cursor:
        _uuid = item.get("uuid")
        _title = item.get("title")
        related_links = item.get("related_url")
        if _uuid and _title and not related_links:
            _title = _title.replace(" ", "_")
            bc = BaiduCrawler()
            urls = bc.get_related_links(_title)
            connect_db.update({"uuid": _uuid},
                          {"$set": {
                              "related_url": urls,
                          }}, upsert=True)
