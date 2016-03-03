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



search_url_gen = lambda x: "http://weixin.sogou.com/weixin?type=1&query={keyword}&ie=utf8".format(keyword=x)





