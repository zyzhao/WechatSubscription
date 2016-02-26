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
import cookielib


reload(sys)
sys.setdefaultencoding("utf-8")

RAND_SLEEP = 1

class WechatCrawler(object):

    def __init__(self, st_dt=0, ed_dt=0, mode="update"):
        self.domain = "http://weixin.sogou.com"
        self.wechat_acct = ""
        self.login_info = ""
        self.st_dt = st_dt if isinstance(st_dt, int) else date_helper.dt_str_to_utc(st_dt)
        self.ed_dt = ed_dt if isinstance(ed_dt, int) else date_helper.dt_str_to_utc(ed_dt)
        self.mode = mode

        cookie = cookielib.CookieJar()
        handler=urllib2.HTTPCookieProcessor(cookie)
        self.opener = urllib2.build_opener(handler)
        # response = opener.open()


    def search(self, keyword="data"):
        url = "http://weixin.sogou.com/weixin?type=1&query={keyword}&ie=utf8".format(keyword=keyword)
        print url
        cookie = cookielib.CookieJar()
        handler=urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)
        # req = requests.get(url)
        # req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36')
        # response = urllib2.urlopen(req)
        req = self.opener.open(url)
        _content = req.read()
        print _content
        soup = BeautifulSoup(_content, 'html')
        wechat_acct = soup.find("label", {"name":"em_weixinhao"}).string
        self.wechat_acct = wechat_acct
        # print soup
        return soup

    def login(self, keyword="data"):
        soup = self.search(keyword)
        res = soup.find("div", {"class":"results"})
        login_param = urlparse(res.div["href"]).query
        self.login_info = login_param
        return login_param

    def get_article_url(self, url="", uuid="_tmp"):
        real_url = ""
        _url = self.domain + url
        req = self.opener.open(_url)
        _content = req.read()
        with open(config.APACHE_DIR + uuid + ".html", "wb") as f:
            f.write(_content)
        # print _content

        return real_url

    def get_articles(self, page, login_info, keyword=""):

        sleep_time = round(np.random.chisquare(RAND_SLEEP), 2)
        print "Let me sleep %s sec." % str(sleep_time)
        time.sleep(sleep_time)

        _end_of_process = False
        _param = "&cb=sogou.weixin_gzhcb&page=%s&gzhArtKeyWord=%s&tsn=3&t=%s&_=%s" % (str(page), keyword, str(self.ed_dt), str(self.st_dt))
        # t=1456382454333&_=1456382454333
        url = self.domain + "/gzhjs?" + login_info + _param
        print url
        # req = requests.get(url)
        req = self.opener.open(url)
        # req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36')
        # response = urllib2.urlopen(req)
        _content = req.read()

        # soup = BeautifulSoup(req.text, 'html')
        _tmp = _content.replace("sogou.weixin_gzhcb(", "")
        _tmp = _tmp.replace(")\n\n\n\n\n\n\n\n\n", "")
        _tmp = _tmp.replace("\\/", "/")
        # print _tmp
        _res_dict = eval(_tmp)

        total_pages = _res_dict.get("totalPages")

        _items = _res_dict.get("items")
        print "Page: %s/%s" % (str(page), str(total_pages))
        # total_pages = 3

        articles = []
        for _item in _items:
            xmlp = ET.XMLParser(encoding="utf-8")
            _item_xml = ET.fromstring(_item, parser=xmlp)
            ref_url = _item_xml.find("item").find("display").find("url").text
            # print _item_xml.find("item").find("display").find("title").text
            # print self.domain + ref_url
            _uuid = make_uuid()
            self.get_article_url(ref_url, _uuid)



            _res = dict(
                uuid=_uuid,
                title=_item_xml.find("item").find("display").find("title").text,
                content=_item_xml.find("item").find("display").find("content168").text,
                url="",
                release_date=_item_xml.find("item").find("display").find("date").text,
                wechat_acct=self.wechat_acct,
                timestamp=date_helper.current_timestamp(),
                unread=True
            )
            with MongodbUtils(config.WECHAT_DB_IP, config.WECHAT_DB_PORT, config.WECHAT_COLLECTION, config.WECHAT_ARTICLE_SUMMARY_TABLE) as connect_db:
                _query = dict(wechat_acct=self.wechat_acct, title=_res.get("title"))
                exist_record = connect_db.find_one(_query)
                if not exist_record:
                    connect_db.insert(_res)
                else:

                    if self.mode in ["init", "overide"]:
                        _end_of_process = False
                        if self.mode in ["overide"]:
                            connect_db.remove(_query)
                            connect_db.insert(_res)
                        else:
                            print "Already exist"
                    else:
                        _end_of_process = True
                        break
            # articles.append(_res)
            # print _res.get("release_date")

        if (page < total_pages) and not _end_of_process:
            self.get_articles(page+1, login_info, keyword)
        else:
            return articles

    def get_wechat_articles(self, keyword=""):
        login_info = self.login(keyword)
        self.get_articles(5, login_info)

if __name__ == "__main__":
    wc = WechatCrawler("2016-02-20", "2016-02-23", mode="init")
    wc.get_wechat_articles("36dashuju")


