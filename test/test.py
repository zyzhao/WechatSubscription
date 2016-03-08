# -*- coding: UTF-8 -*-
import re
import os
import sys
import urllib
import urllib2
import requests
from datetime import *
from bs4 import BeautifulSoup
from pymongo import MongoClient
from urlparse import urlparse, parse_qs
import xml.etree.ElementTree as ET


reload(sys)
sys.setdefaultencoding("utf-8")

domain = "http://weixin.sogou.com"
start_url = "http://weixin.sogou.com/weixin?type=1&query={keyword}&ie=utf8".format(keyword="dashuju36")
print start_url

req = requests.get(start_url)
print req.text

soup = BeautifulSoup(req.text, 'html')

_res = soup.find("div", {"class":"results"})
_res.div["href"]


logging_param = urlparse(_res.div["href"]).query
drilldown_url = domain + "/gzhjs?" + logging_param


print drilldown_url + "&cb=sogou.weixin_gzhcb&page=2&gzhArtKeyWord=&tsn=0"
req = requests.get(drilldown_url + "&cb=sogou.weixin_gzhcb&page=1&gzhArtKeyWord=&tsn=0")

soup_pub = BeautifulSoup(req.text, 'html')


_tmp = req.text.replace("sogou.weixin_gzhcb(", "")
_tmp = _tmp.replace(")\n\n\n\n\n\n\n\n\n", "")
_tmp = _tmp.replace("\\/", "/")
_items = eval(_tmp).get("items")

xmlp = ET.XMLParser(encoding="utf-8")
_item_soup = ET.fromstring(_items[0], parser=xmlp)


for i in _item_soup.find("item").find("display"):
    print i

print _item_soup.find("item").find("display").find("title").text
print _item_soup.find("item").find("display").find("content168").text
print _item_soup.find("item").find("display").find("url").text

print _items[0][50:60]

_item_soup = ET.fromstring(_items[0])


print "\\/".replace("\\/","/")

"http://weixin.sogou.com/gzhjs?openid=oIWsFt5eUeW0inpzNKVIuiCwATo8&ext=pbbx73yLDYaxA67fYtxUzjr0KbAkpf2dCkDdoyX_hKmBRrhjAxadMIN0OM15Pmy3&cb=sogou.weixin_gzhcb&page=2&gzhArtKeyWord=&tsn=0"






url_1 = "http://weixin.sogou.com/gzhjs?openid=oIWsFt5WygjVSXqvAXXD7R5-6Y1g&ext=_vj5mXzN99o8IjhoEFbQwfxC06iS0qqjiydrMssP0upZrrADq3RsQplSBg41II2h&cb=sogou.weixin_gzhcb&tsn=3&page=3"

import urllib2
import cookielib
#声明一个CookieJar对象实例来保存cookie
cookie = cookielib.CookieJar()
#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler=urllib2.HTTPCookieProcessor(cookie)
#通过handler来构建opener
opener = urllib2.build_opener(handler)
#此处的open方法同urllib2的urlopen方法，也可以传入request
response = opener.open(url_1)
for item in cookie:
    print 'Name = '+item.name
    print 'Value = '+item.value

xxx = response.read()

_tmp = xxx.replace("sogou.weixin_gzhcb(", "")
_tmp = _tmp.replace(")\n\n\n\n\n\n\n\n\n", "")
_tmp = _tmp.replace("\\/", "/")
_items = eval(_tmp).get("items")

xmlp = ET.XMLParser(encoding="utf-8")
_item_soup = ET.fromstring(_items[0], parser=xmlp)


def get_xml_node(xml=None, path=""):
    _node_cursor = xml.find(path)
    try:
        res = _node_cursor.text
    except:
        res = ""
    return res

test_r = get_xml_node(_item_soup, "item/display/title")
print test_r

print _item_soup.find("item/display/title").text


# for i in _item_soup.find("item").find("display"):
#     print i
#
# print _item_soup.find("item").find("display").find("title").text
# print _item_soup.find("item").find("display").find("content168").text
# print _item_soup.find("item").find("display").find("url").text


url_2 = "http://weixin.sogou.com" + _item_soup.find("item").find("display").find("url").text

response = opener.open(url_2)
xxx2 = response.read()

with open("test.html", "wb") as f:
    f.write(xxx2)

print xxx2

urllib.urlretrieve(url_2, "/Library/WebServer/Documents/wechat/doc.html")


url = "http://weixin.sogou.com/weixin?type=1&query={keyword}&ie=utf8".format(keyword="36dashuju")
_headers = {
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
wechat_name = soup.find("em")
print wechat_name.text
self.wechat_acct = wechat_acct
self.wechat_name = wechat_name
# print soup




_url = "http://weixin.sogou.com/websearch/art.jsp?sg=CBf80b2xkgZJPlPSlsWKqbiXL89_EussXTehg5mH1sxSbqpP7ReSBFcPOf-qFxtou1zCwy9uTmEDeZssqz-ioM17F1zzVD8WR2rqNa8sOs_o2d2w2y2QDuy66BWGbZ2NZJ_Hf_9xG40.&url=p0OVDH8R4SHyUySb8E88hkJm8GF_McJfBfynRTbN8wh_lRut3_CVLxUChivsk6qdTlCIIgb6R88hOD6_FrmEkWQ3JxMQ3374CJCuCy0w0Q5vLnR12SkXHTD0Ct4iq2QcX5USEMYJaK1Yy-5x5In7jJFmExjqCxhpkyjFvwP6PuGcQ64lGQ2ZDMuqxplQrsbk"


req = urllib2.Request(_url, None, _headers)
response = urllib2.urlopen(req)
_content = response.read()




# localhost/wechat/4c15ceca-df5a-11e5-8038-000ec6c3b5cf-1310.html




def print_arg(func):
    # @wraps(func)
    def catch_error(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            print args
            print kwargs
        except Exception as e:
            # print traceback.format_exc()
            return None
        return res
    return catch_error

@print_arg
def test_arg(a,b,c=1,d=2):
    pass

test_arg(1,2,c=3,d=4)


url = "http://www.baidu.com/link?url=WDa5mcjqYSIk79zr3NZ1m9aO5gfyon6qxOjvWHAJW-_7xAf2RE5xAWDEewZiZbu6MTm7L8pN-7SUSIh8nCKTl_"


import requests
import urllib2

req = urllib2.Request(url)
response = urllib2.urlopen(req)
_content = response.read()

response["Location"]



requests.head(url).headers["location"]



