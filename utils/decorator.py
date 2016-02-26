# -*- coding: utf-8 -*-
from functools import wraps
import traceback
import threading
import time
import json
import date_helper

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
