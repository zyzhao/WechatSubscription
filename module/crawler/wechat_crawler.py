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

reload(sys)
sys.setdefaultencoding("utf-8")

RAND_SLEEP = 2

class WechatCrawler(object):
    def __init__(self, st_dt=0, ed_dt=0, mode="update"):
        self.domain = "http://weixin.sogou.com"
        self.wechat_acct = ""
        self.wechat_name = ""
        self.login_info = ""
        self.keyword = ""
        self.st_dt = st_dt if isinstance(st_dt, int) else date_helper.dt_str_to_utc(st_dt)
        self.ed_dt = ed_dt if isinstance(ed_dt, int) else date_helper.dt_str_to_utc(ed_dt)
        self.mode = mode
        self.url_generator = None
        self.url_generator_js = None

        cookie = cookielib.CookieJar()
        handler = urllib2.HTTPCookieProcessor(cookie)
        self.opener = urllib2.build_opener(handler)
        # response = opener.open()

        self.browser = WebBrowser()

    @simulate_human(5, 10)
    def browser_search(self, keyword="data"):
        self.keyword = keyword
        url = "http://weixin.sogou.com/weixin?type=1&query={keyword}&ie=utf8".format(keyword=keyword)
        LOG.info("Search Keyword [%s]: %s" % (keyword, url))

        # _headers = self.head
        # req = urllib2.Request(url, None, _headers)
        # response = urllib2.urlopen(req)
        # _content = response.read()

        _content = self.browser.get_url_content(url)

        return _content

    @try_except_parse
    def parse_acct_search(self, content="", save=True):
        _content = content
        soup = BeautifulSoup(_content, 'html')
        wechat_acct = soup.find("label", {"name": "em_weixinhao"}).text
        wechat_name = soup.find("em").text
        self.wechat_acct = wechat_acct
        self.wechat_name = wechat_name
        res = soup.find("div", {"class": "results"})
        login_param = urlparse(res.div["href"]).query
        self.login_info = login_param
        if self.wechat_acct and self.login_info and save:
            with MongodbUtils(config.WECHAT_DB_IP, config.WECHAT_DB_PORT, config.WECHAT_COLLECTION,
                              config.WECHAT_ACCOUNT_TABLE) as connect_db:
                _res = connect_db.find_one({"account": self.wechat_acct})
                # acct_param = _res.get("param", "")
                if not _res:
                    connect_db.update({"account": self.wechat_acct},
                                      {"$set": {
                                          "keyword": self.keyword,
                                          "account": self.wechat_acct,
                                          "url_param": login_param,
                                          "account_name": self.wechat_name,
                                          "real_acct": self.wechat_acct,
                                          "category": "",
                                          "tag": [],
                                      }}, upsert=True)
                    LOG.info("%s is add to the database" % (self.wechat_acct))
                else:
                    LOG.info("%s is already in the database" % (self.wechat_acct))
        return login_param

    def act_search_account(self, account):
        _content = self.browser_search(account)
        login_param = self.parse_acct_search(_content)
        return login_param

    def load_account_info(self, account):
        url_generator_js = None
        url_generator = None
        with MongodbUtils(config.WECHAT_DB_IP, config.WECHAT_DB_PORT, config.WECHAT_COLLECTION,
                          config.WECHAT_ACCOUNT_TABLE) as connect_db:
            _res = connect_db.find_one({"account": account})
        if _res:
            _acct_param = _res.get("url_param", "")
            wechat_acct = _res.get("account")
            wechat_name = _res.get("account_name")
            if _acct_param:
                # _param_ = "&cb=sogou.weixin_gzhcb&gzhArtKeyWord=%s&tsn=3&t=&_=&page="
                _param_ = "&cb=sogou.weixin_gzhcb&tsn=3&page="

                LOG.info("Infomation of account [%s] was loaded." % (account))
                url_generator_js = lambda x: self.domain + "/gzhjs?" + _acct_param + _param_ + str(x)
                url_generator = lambda x: self.domain + "/gzh?" + _acct_param + _param_ + str(x)
            else:
                LOG.info("Account [%s] does not have login param." % (account))
        else:
            LOG.info("Account [%s] was not found." % (account))
        self.wechat_acct = wechat_acct
        self.wechat_name = wechat_name
        self.url_generator = url_generator
        self.url_generator_js = url_generator_js

    @simulate_human(30, 10)
    def browser_account_page(self, page=1):
        url = self.url_generator_js(page)
        LOG.info("Visit account page: %s " % (url))
        _content = self.browser.get_url_content(url)
        return _content

    @try_except_parse
    def parse_account_page(self, content):
        _end_of_process = False
        _tmp = content.replace("sogou.weixin_gzhcb(", "")
        _tmp = _tmp.replace(")\n\n\n\n\n\n\n\n\n", "")
        _tmp = _tmp.replace("\\/", "/")
        _res_dict = eval(_tmp)

        # Get pagination infomation
        total_pages = _res_dict.get("totalPages")
        page = _res_dict.get("page")
        _end_of_process = True if page >= total_pages else False

        LOG.info("Page: %s/%s" % (str(page), str(total_pages)))

        # Get articles on page
        _items = _res_dict.get("items")
        num_of_articles_downloaded = 0
        for _item in _items:
            xmlp = ET.XMLParser(encoding="utf-8")
            _item_xml = ET.fromstring(_item, parser=xmlp)
            _uuid = make_uuid()

            _res = dict(
                uuid=_uuid,
                title=self.browser.get_xml_node(_item_xml, "item/display/title"),
                content=_item_xml.find("item").find("display").find("content168").text,
                site=self.browser.get_xml_node(_item_xml, "item/display/site"),
                url=self.browser.get_xml_node(_item_xml, "item/display/url"),
                sourcename=self.browser.get_xml_node(_item_xml, "item/display/sourcename"),
                release_date=self.browser.get_xml_node(_item_xml, "item/display/date"),
                wechat_acct=self.wechat_acct,
                timestamp=date_helper.current_timestamp(),
                unread=True,
                tag=[]
            )

            LOG.info("Reading article: %s" % (_res.get("title")))
            LOG.info("Source site: %s" % (_res.get("site")))
            LOG.info("From: %s" % (_res.get("wechat_acct")))

            with MongodbUtils(config.WECHAT_DB_IP, config.WECHAT_DB_PORT, config.WECHAT_COLLECTION,
                              config.WECHAT_ARTICLE_SUMMARY_TABLE) as connect_db:
                _query = dict(wechat_acct=self.wechat_acct, title=_res.get("title"))
                exist_record = connect_db.find_one(_query)

                if not exist_record or self.mode == 'init':
                    if self.mode == 'init' and exist_record:
                        _old_uuid = exist_record.get("uuid", "")
                        _res["uuid"] = _old_uuid
                        connect_db.remove(_query)

                    connect_db.insert(_res)
                    if not _res.get("site"):
                        self.download_article_content(_res)
                    # _article_url = self.get_article_url(_res.get("site"), _uuid)
                    # if _article_url:
                    #     num_of_articles_downloaded += 1
                else:
                    _end_of_process = True
                    break
        return _end_of_process

    @simulate_human(30, 15)
    def download_article_content(self, item):
        article_url = item.get("url", "")
        refer_url = item.get("site", "")
        uuid = item.get("uuid", "")

        if not refer_url:
            LOG.info("There is not refered URL. Try to download the content through original url")
            _url = self.domain + article_url
            article_content = self.browser.get_url_content(_url)
            with open(config.APACHE_DIR + uuid + ".html", "wb") as f:
                f.write(article_content)
            res = "download"
        else:
            LOG.info("Article is refered. No need to download the content")
            res = "refer"
        return res

    def run_crawl_account_articles(self, account):
        self.load_account_info(account)

        if self.url_generator_js and self.wechat_acct:
            self.update_accout_status(self.wechat_acct, "Running")
            _page = 1
            _end_process = False
            while (not _end_process):
                _acct_page_content = self.browser_account_page(_page)
                _end_process = self.parse_account_page(_acct_page_content)
                if _page > 5 and not _end_process:
                    _end_process = True
                _page += 1
            self.update_accout_status(self.wechat_acct, "Done")
        return None

    def update_accout_status(self, account, status):
        if account and status:
            with MongodbUtils(config.WECHAT_DB_IP, config.WECHAT_DB_PORT, config.WECHAT_COLLECTION,
                              config.WECHAT_ACCOUNT_TABLE) as connect_db:
                connect_db.update({"account": account}, {"$set":{
                    "status": status,
                    "timestamp": date_helper.current_timestamp(),
                    "timestamp_str": date_helper.current_date()
                }})



    def get_article_url(self, url="", uuid="_tmp"):
        real_url = ""
        # _url = self.domain + url
        _url = url
        print _url
        # req = self.opener.open(_url)
        # _content = req.read()

        # _headers = self.head
        # req = urllib2.Request(_url, None, _headers)
        # response = urllib2.urlopen(req)
        # _content = response.read()

        _content = self.get_url_content(_url, self.head2)

        with open(config.APACHE_DIR + uuid + ".html", "wb") as f:
            f.write(_content)
        return real_url

    @try_except
    def get_articles_on_page(self, page=1):
        _end_of_process = False
        url = self.url_generator_js(page)
        print url
        _content = self.get_url_content(url)
        print _content

        # soup = BeautifulSoup(req.text, 'html')
        _tmp = _content.replace("sogou.weixin_gzhcb(", "")
        _tmp = _tmp.replace(")\n\n\n\n\n\n\n\n\n", "")
        _tmp = _tmp.replace("\\/", "/")
        _res_dict = eval(_tmp)
        # print _content

        total_pages = _res_dict.get("totalPages")
        page = _res_dict.get("page")
        _items = _res_dict.get("items")
        LOG.info("Page: %s/%s" % (str(page), str(total_pages)))
        # total_pages = 3

        articles = []
        num_of_articles_downloaded = 0
        for _item in _items:
            xmlp = ET.XMLParser(encoding="utf-8")
            _item_xml = ET.fromstring(_item, parser=xmlp)
            ref_url = _item_xml.find("item").find("display").find("url").text
            _uuid = make_uuid()

            # print _item_xml.find("item").find("display").text
            print "--------start test------"
            print self.get_xml_node(_item_xml, "item/display/title")
            print self.get_xml_node(_item_xml, "item/display/site")
            print "--------end test------"
            _res = dict(
                uuid=_uuid,
                title=self.get_xml_node(_item_xml, "item/display/title"),
                content=_item_xml.find("item").find("display").find("content168").text,
                site=self.get_xml_node(_item_xml, "item/display/site"),
                url=self.get_xml_node(_item_xml, "item/display/url"),
                sourcename=self.get_xml_node(_item_xml, "item/display/sourcename"),
                release_date=self.get_xml_node(_item_xml, "item/display/date"),
                wechat_acct=self.wechat_acct,
                timestamp=date_helper.current_timestamp(),
                unread=True,
                tag=[]
            )
            # print _res.get("title")

            with MongodbUtils(config.WECHAT_DB_IP, config.WECHAT_DB_PORT, config.WECHAT_COLLECTION,
                              config.WECHAT_ARTICLE_SUMMARY_TABLE) as connect_db:
                _query = dict(wechat_acct=self.wechat_acct, title=_res.get("title"))
                exist_record = connect_db.find_one(_query)

                if not exist_record or self.mode == 'override':
                    if self.mode == 'override':
                        _old_uuid = exist_record.get("uuid", "")
                        _res["uuid"] = _old_uuid
                        connect_db.remove(_query)

                    connect_db.insert(_res)
                    # _article_url = self.get_article_url(_res.get("site"), _uuid)
                    # if _article_url:
                    #     num_of_articles_downloaded += 1
                else:
                    if self.mode in ["init"]:
                        _end_of_process = False
                        LOG.info("Already exist")
                    else:
                        _end_of_process = True
                        LOG.info("Meet the last article in DB")
                        break

        LOG.info("%s pages are downloaded on this page" % num_of_articles_downloaded)

        if (page < total_pages) and not _end_of_process:
            LOG.info("Go to next page")
            self.get_articles_on_page(page + 1)
        else:
            return articles

    def run_acct_crawler(self, account=""):
        acct = account if account else self.self.wechat_acct
        self.get_account_page(acct)
        url_login = self.url_generator(1)
        login_info = self.get_url_content(url_login)
        # print login_info
        self.get_articles_on_page()



    # =================== BAK ===================
    def login(self, keyword="data"):
        soup = self.search(keyword)
        res = soup.find("div", {"class": "results"})
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

    def get_wechat_articles(self, keyword=""):
        LOG.info("Start to get data of account [%s]" % (keyword))
        login_info = self.login(keyword)
        LOG.info("Finished getting login param of account [%s]" % (keyword))
        self.get_articles(1, login_info)
        LOG.info("End process for account [%s]" % (keyword))


if __name__ == "__main__":
    wc = WechatCrawler("2016-02-20", "2016-02-23", mode="init")
    wc.run_crawl_account_articles("DataScientistUnion")
    # wc.load_account_info("datahub")
    # acct_list = [u"36大数据", u"数盟", u"咖啡沙龙"]
    # for _acct in acct_list:
    #     wc.search_account(_acct)
    #     sleep_time = round(np.random.chisquare(RAND_SLEEP), 5) + 10
    #     time.sleep(sleep_time)

    # wc.get_wechat_articles("36dashuju")
    # _c = wc.search(u"数盟")
    # print wc.parse_acct_search(_c)
    # print wc.get_account_page("dashuju36")(1)
    # print wc.get_account_page("dashuju36")(2)
    # wc.run_acct_crawler("dashuju36")
    # wc.run_acct_crawler("DataScientistUnion")
