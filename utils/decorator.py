# -*- coding: utf-8 -*-
from functools import wraps
import traceback
import threading
import time
import json
import date_helper
from utils.log import LOG
import numpy as np

def get_func_time(func):
    @wraps(func)
    def record_time(*args, **kwargs):
        class_name=""
        if len(args) > 0:
            # print str(type(args[0]))
            # if str(type(args[0])) == "<type 'instance'>":
            class_name = args[0].__class__.__name__
        if class_name:
            func_name = "%s.%s" % (class_name, func.__name__)
        else:
            func_name = func.__name__

        print "[%s] Start" % func_name
        st = date_helper.current_date()
        res = func(*args, **kwargs)
        # print args[0].__class__.__name__
        ed = date_helper.current_date()
        time_diff = date_helper.date_time_span(ed, st)
        print "[%s] Finished (%s sec used)" % (func_name, str(time_diff))
        return res
    return record_time


def try_except(func):
    """
    传统的捕获异常

    :param func:
    :return:
    """
    @wraps(func)
    def catch_error(*args, **kwargs):
        try:
            res = func(*args, **kwargs)

        except Exception as e:
            LOG.error(traceback.format_exc())
            # print traceback.format_exc()
            return None
        return res
    return catch_error


def try_except_parse(func):
    """
    出现解析异常时打印content

    :param func:
    :return:
    """
    @wraps(func)
    def catch_error(*args, **kwargs):
        try:
            res = func(*args, **kwargs)

        except Exception as e:
            LOG.error(traceback.format_exc())
            LOG.info("================content start================")
            _content = kwargs.get("content")
            _content = _content if _content else args[0]
            print _content
            LOG.info("================content end================")
            return None
        return res
    return catch_error



def simulate_human(seed, offset):
    def auto_sleep(func):
        @wraps(func)
        def record_time(*args, **kwargs):
            res = func(*args, **kwargs)
            sleep_time = round(np.random.chisquare(seed), 2) + offset
            LOG.info("I'm gona to sleep for %s sec." % (str(sleep_time)))
            time.sleep(sleep_time)
            return res
        return record_time
    return auto_sleep



if __name__ == "__main__":

    @get_func_time
    def test2(a,d = 1):
        pass

    class DecTest():

        @get_func_time
        def test(self, aa=0):
            pass

    DecTest().test()
    # test2(1,2)
