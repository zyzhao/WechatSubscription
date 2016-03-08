# -*- coding: UTF-8 -*-
import sys
import requests
import pandas as pd
import re
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
import Levenshtein

reload(sys)
sys.setdefaultencoding("utf-8")

RAND_SLEEP = 2


class BaiduCrawler(object):
    def __init__(self):
        self.domain = "http://www.baidu.com"
        self.search_url_generator = lambda x: self.domain + "/s?wd={keyword}".format(keyword=x)
        self.keyword = None

        self.browser = WebBrowser()

    @simulate_human(3, 2)
    def browser_search(self, keyword="data", page=1):
        self.keyword = keyword
        url = self.search_url_generator(self.keyword)
        url = url.replace(" ", "%20")
        if page > 1:
            url += "pn=%s" % (str((page-1)*10))
        LOG.info("Search Keyword [%s]: %s" % (keyword, url))
        _content = self.browser.get_url_content(url)
        return _content


    @try_except_parse
    def parse_search_result(self, content=""):
        _content = content
        soup = BeautifulSoup(_content, 'html')
        # print soup
        _res_content = soup.find("div", {"id": "content_left"})
        _res_list = _res_content.children
        results = []
        for item in _res_list:
            try:
                _url = item.h3.a["href"]
                # print _url
                _title =  item.h3.a.text
                _id = item.get("id")
                simularity = Levenshtein.ratio(_title, self.keyword)
                _real_url =  self.find_redirect_url(_url)
                LOG.info( "[%s]" % str(_id) + _title + "(%s)" % str(simularity))
                res = dict(
                    title=_title,
                    rank=_id,
                    simularity=simularity,
                    baidu_url=_url,
                    url=_real_url
                )
            except:
                res = dict(title="", rank=0, simularity=0, baidu_url="", url="" )
                # print "[Failed to parse the item]"
                # print item
                pass
            results.append(res)

        return results

    def analysis_search_result(self, results):
        urls = []
        if results:
            df = pd.DataFrame(results)
            df.sort(columns=["simularity"], ascending=False)
            urls = df["url"][:5].tolist()
        return urls


    @simulate_human(1, 0)
    def find_redirect_url(self, url):
        _url = requests.head(url).headers["location"]
        #
        # _content = self.browser.get_url_content(url)
        # soup = BeautifulSoup(_content)
        # # print soup.noscript
        # _s = str(soup.noscript)
        # print soup
        # result = re.findall(".*URL='(.*)'.*", _s)
        return _url

    def get_related_links(self, title):
        _c = self.browser_search(title, 1)
        res = self.parse_search_result(_c)
        urls = self.analysis_search_result(res)
        return urls


if __name__ == "__main__":
    bc = BaiduCrawler()
    _c = bc.get_related_links(u"华为电脑要做世界第一?HUAWEIMateBook在你的剁手清...")
    print _c
    # res = bc.parse_search_result(_c)
    # bc.analysis_search_result(res)
    # bc.find_redirect_url("http://www.baidu.com/link?url=WDa5mcjqYSIk79zr3NZ1m9aO5gfyon6qxOjvWHAJW-_7xAf2RE5xAWDEewZiZbu6MTm7L8pN-7SUSIh8nCKTl_")






