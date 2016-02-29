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
from utils.log import LOG

reload(sys)
sys.setdefaultencoding("utf-8")

RAND_SLEEP = 1

class WechatCrawler(object):

    def __init__(self, st_dt=0, ed_dt=0, mode="update"):
        self.domain = "http://weixin.sogou.com"
        self.wechat_acct = ""
        self.wechat_name = "s"
        self.login_info = ""
        self.st_dt = st_dt if isinstance(st_dt, int) else date_helper.dt_str_to_utc(st_dt)
        self.ed_dt = ed_dt if isinstance(ed_dt, int) else date_helper.dt_str_to_utc(ed_dt)
        self.mode = mode

        cookie = cookielib.CookieJar()
        handler=urllib2.HTTPCookieProcessor(cookie)
        self.opener = urllib2.build_opener(handler)
        # response = opener.open()

        self.head = {
            # 'Accept-Encoding':"gzip, deflate, sdch",
            # 'Accept-Language':"en,zh-CN;q=0.8,zh;q=0.6",
            # 'Cache-Control':"max-age=0",
            # 'Connection':"keep-alive",
            'Cookie':"ABTEST=0|1456478015|v1; IPLOC=CN3100; SUID=CF4351652624930A0000000056D0173F; PHPSESSID=t7ok6mfp3d2n7jhela6gk4ti12; SUIR=1456478015; SUID=CF4351654418920A0000000056D0173F; SUV=00C21B41655143CF56D01771F0552708; SNUID=47CBD8ED898DA42159C15537898A2903; seccodeRight=success; successCount=1|Fri, 26 Feb 2016 09:25:44 GMT",
            'Host':"weixin.sogou.com",
            # 'If-Modified-Since':"Wed, 14 Oct 2015 06:39:57 GMT",
            # 'Referer':"http://weixin.sogou.com/weixin?type=1&query=36dashuju&ie=utf8",
            'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36",
        }


    def search(self, keyword="data"):
        url = "http://weixin.sogou.com/weixin?type=1&query={keyword}&ie=utf8".format(keyword=keyword)
        LOG.info("Search Keyword: %s" % keyword)
        _headers = self.head
        req = urllib2.Request(url, None, _headers)
        response = urllib2.urlopen(req)
        _content = response.read()

        # cookie = cookielib.CookieJar()
        # handler=urllib2.HTTPCookieProcessor   (cookie)
        # opener = urllib2.build_opener(handler)
        # # req = requests.get(url)
        # # req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36')
        # # response = urllib2.urlopen(req)
        # req = self.opener.open(url)
        # _content = req.read()
        # print _content
        soup = BeautifulSoup(_content, 'html')
        wechat_acct = soup.find("label", {"name":"em_weixinhao"}).string
        wechat_name = soup.find("em").text
        self.wechat_acct = wechat_acct
        self.wechat_name = wechat_name
        # print soup
        return soup

    def login(self, keyword="data"):
        soup = self.search(keyword)
        res = soup.find("div", {"class":"results"})
        login_param = urlparse(res.div["href"]).query
        self.login_info = login_param
        with MongodbUtils(config.WECHAT_DB_IP, config.WECHAT_DB_PORT, config.WECHAT_COLLECTION,
                          config.WECHAT_ACCOUNT_TABLE) as connect_db:
            _res = connect_db.find_one({"account": keyword})
            acct_param = _res.get("param", "")
            if not acct_param:
                connect_db.update({"account": keyword},
                                  {"$set": {
                                      "param": login_param,
                                      "account_name": self.wechat_name,
                                      "real_acct": self.wechat_acct
                                  }})

        return login_param

    def get_article_url(self, url="", uuid="_tmp"):
        real_url = ""
        _url = self.domain + url
        req = self.opener.open(_url)
        _content = req.read()
        with open(config.APACHE_DIR + uuid + ".html", "wb") as f:
            f.write(_content)
        return real_url

    def get_articles(self, page, login_info, keyword=""):
        sleep_time = round(np.random.chisquare(RAND_SLEEP), 2)
        # print "Let me sleep %s sec." % str(sleep_time)
        time.sleep(sleep_time)

        _end_of_process = False
        _param = "&cb=sogou.weixin_gzhcb&page=%s&gzhArtKeyWord=%s&tsn=3&t=%s&_=%s" % (str(page), keyword, str(self.ed_dt), str(self.st_dt))
        # t=1456382454333&_=1456382454333
        url = self.domain + "/gzhjs?" + login_info + _param
        LOG.info("Crawling URL: " + url)
        # req = requests.get(url)
        req = self.opener.open(url)
        # req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36')
        # response = urllib2.urlopen(req)
        _content = req.read()

        # soup = BeautifulSoup(req.text, 'html')
        _tmp = _content.replace("sogou.weixin_gzhcb(", "")
        _tmp = _tmp.replace(")\n\n\n\n\n\n\n\n\n", "")
        _tmp = _tmp.replace("\\/", "/")
        _res_dict = eval(_tmp)

        total_pages = _res_dict.get("totalPages")

        _items = _res_dict.get("items")
        LOG.info( "Page: %s/%s" % (str(page), str(total_pages)))
        # total_pages = 3

        articles = []
        num_of_articles_downloaded = 0
        for _item in _items:
            xmlp = ET.XMLParser(encoding="utf-8")
            _item_xml = ET.fromstring(_item, parser=xmlp)
            ref_url = _item_xml.find("item").find("display").find("url").text
            # print _item_xml.find("item").find("display").find("title").text
            # print self.domain + ref_url
            _uuid = make_uuid()

            _res = dict(
                uuid=_uuid,
                title=_item_xml.find("item").find("display").find("title").text,
                content=_item_xml.find("item").find("display").find("content168").text,
                url="",
                release_date=_item_xml.find("item").find("display").find("date").text,
                wechat_acct=self.wechat_acct,
                timestamp=date_helper.current_timestamp(),
                unread=True,
                tag=[]
            )
            with MongodbUtils(config.WECHAT_DB_IP, config.WECHAT_DB_PORT, config.WECHAT_COLLECTION, config.WECHAT_ARTICLE_SUMMARY_TABLE) as connect_db:
                _query = dict(wechat_acct=self.wechat_acct, title=_res.get("title"))
                exist_record = connect_db.find_one(_query)
                if not exist_record:
                    connect_db.insert(_res)
                    _article_url = self.get_article_url(ref_url, _uuid)
                    if _article_url:
                        num_of_articles_downloaded += 1
                else:

                    if self.mode in ["init", "override"]:
                        _end_of_process = False
                        if self.mode in ["override"]:
                            _old_uuid = exist_record.get("uuid", "")
                            _res["uuid"] = _old_uuid
                            connect_db.remove(_query)
                            connect_db.insert(_res)
                            _article_url = self.get_article_url(ref_url, _old_uuid)
                            if _article_url:
                                num_of_articles_downloaded += 1
                        else:
                            LOG.info("Already exist")

                    else:
                        _end_of_process = True
                        LOG.info("Meet the last article in DB")
                        # LOG.info("End Process")
                        break
            # articles.append(_res)
        LOG.info("%s pages are downloaded on this page" % num_of_articles_downloaded)

        if (page < total_pages) and not _end_of_process:
            LOG.info("Go to next page")
            self.get_articles(page+1, login_info, keyword)
        else:
            return articles

    def get_wechat_articles(self, keyword=""):
        LOG.info("Start to get data of account [%s]" % (keyword))
        login_info = self.login(keyword)
        LOG.info("Finished getting login param of account [%s]" % (keyword))
        self.get_articles(1, login_info)
        LOG.info("End process for account [%s]" % (keyword))

if __name__ == "__main__":
    wc = WechatCrawler("2016-02-20", "2016-02-23", mode="update")
    wc.get_wechat_articles("36dashuju")


