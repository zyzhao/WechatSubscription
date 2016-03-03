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
from utils.decorator import try_except
import utils.date_helper as date_helper
import urllib2
import cookielib
from utils.log import LOG
import traceback

reload(sys)
sys.setdefaultencoding("utf-8")


class WebBrowser(object):
    def __init__(self):

        cookie = cookielib.CookieJar()
        handler = urllib2.HTTPCookieProcessor(cookie)
        self.opener = urllib2.build_opener(handler)
        # response = opener.open()

        self.head2 = {
            'Cookie': "pgv_pvi=330661888; pgv_si=s6661668864; ptisp=ctc; ptui_loginuin=387740662; pt2gguin=o0387740662; uin=o0387740662; skey=@Gp8EgYCB4; RK=rFkjyoLWdb; ptcz=64f8fcaa439df272a45a3b7320c56196dc0e5d7f4c68c213ea827a997f2fede3"
        }

        self.head = {
            'Cookie': "ABTEST=7|1456134765|v1; SNUID=F12E50C5B2B79E560FC1AC90B2E3AF05; IPLOC=CN3100; SUID=9A56E2742708930A0000000056CADA6D; SUID=9A56E2743108990A0000000056CADA6E; SUV=1456134766298852; weixinIndexVisited=1; sct=9; ppinf=5|1456800805|1458010405|Y2xpZW50aWQ6NDoyMDE3fGNydDoxMDoxNDU2ODAwODA1fHJlZm5pY2s6NjpRUVVzZXJ8dHJ1c3Q6MToxfHVzZXJpZDo0NDoxNDU3NUE0Q0NEMzAzQTYyNUI5MzBCRDI2MzIyODhCRkBxcS5zb2h1LmNvbXx1bmlxbmFtZTo2OlFRVXNlcnw; pprdig=RDdHzLR9xsKAgn-8XVonmlCxv3IogL4dGT0uHKepWGVKvdwYj2Flj9JbEyOF5P2-THs-wAOeABvGB7_AcD5GTeN28NsFqgEyNGI2ArSMSYAbuXz6nlUaDQiSMb2zcGOWDPXeISWtF5geWKU_c9WeWDiOG1lNMcgfuIMYz1034Mw; ppmdig=1456800805000000914f230d2b9dba597548214c2964adc6; LSTMV=1065%2C276; LCLKINT=2438",
            # 'Host':"weixin.sogou.com",
            # 'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36",
        }


    def get_url_content(self, url, head={}):
        LOG.info("Visit URL: %s" % url)
        _headers = head if head else self.head
        req = urllib2.Request(url, None, _headers)
        response = urllib2.urlopen(req)
        # req = requests.get(url)
        _content = response.read()
        # req = self.opener.open(url)
        # _content = req.read()
        return _content

    def get_xml_node(self, xml=None, path=""):
        _node_cursor = xml.find(path)
        try:
            res = _node_cursor.text
        except:
            res = ""
        return res

    def simulate_sleep(self, m=5, offset=10):
        sleep_time = round(np.random.chisquare(m), 2) + offset
        LOG.info("I'm gona to sleep for %s sec." % (str(sleep_time)))
        time.sleep(sleep_time)




