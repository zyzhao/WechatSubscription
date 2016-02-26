# -*- coding: utf-8 -*-
# @note: 定义报告输出的结果
import datetime
import time
import math
import pytz
from dateutil.rrule import *
from dateutil.parser import parse
from dateutil.relativedelta import *
from collections import OrderedDict

tz = pytz.timezone(pytz.country_timezones('cn')[0])


# @return: 当前的datetime时间戳
def now_dt():
    return datetime.datetime.now()


# 当前时间
def current_date():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def current_day():
    return datetime.datetime.now().strftime('%Y-%m-%d')


def current_timestamp():

    current_timestamp = int(time.time() * 1000)

    return current_timestamp


def today_timestamp():
    """
    今日凌晨时间戳

    :return:
    """
    nd = now_date()
    nd_str = get_dt_day(nd)
    nd_timestamp = date_str_transfer_timestamp(nd_str)

    return nd_timestamp


def next_n_days_timestamp(days=1):
    """
    距离今日n天后的时间戳

    :param days:
    :return:
    """

    next_n_days_date = datetime.date.today() + datetime.timedelta(days=days)
    nnd_str = get_dt_day(next_n_days_date)
    nnd_timestamp = date_str_transfer_timestamp(nnd_str)

    return nnd_timestamp


# @return: 当前的date
def now_date():
    return datetime.datetime.now().date()


# @return: 返回1970.01.01，datetime类型
def null_dt():
    return datetime.datetime(1970, 1, 1)


# @return: 返回1970.01.01，date类型
def null_date():
    return datetime.date(1970, 1, 1)


# @param: 输入日期格式，
# @return: datetime类型
def get_dt(dt_str="1970-01-01 00:00:00", dt_format='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.strptime(dt_str, dt_format)


# @param: 输入日期格式，
# @return: date类型
def get_date(date_str="1970-01-01", dt_format='%Y-%m-%d'):
    return get_dt(date_str, dt_format).date()


def get_dt_day(dt, dt_format='%Y-%m-%d'):
    return dt.strftime(dt_format)


# @param: datetime

# @return: string类型
def get_dt_mth(dt, dt_format='%Y-%m'):
    return dt.strftime(dt_format)


# @param: datetime
# @return: string类型
def get_dt_str(dt, dt_format="%Y-%m-%d %H:%M:%S"):
    return dt.strftime(dt_format)


def date_str_transfer_timestamp(date_str):
    tstamp = None
    if date_str:
        tstamp = int(time.mktime(time.strptime(date_str, '%Y-%m-%d')) * 1000)

    return tstamp


# 时间区间列表
# 参数目前mins_delta 默认间隔60分钟
# 00:00:00-01:00:00 含义为在区间00:00:00<=x< 01:00:00
def create_time_zone_range(mins_delta=60):
    time_list = list(rrule(MINUTELY, interval=mins_delta, dtstart=parse('1970-01-01'), until=parse('1970-01-02')))
    time_str_list = [tl.strftime("%H:%M:%S") for tl in time_list]

    time_period_list = []
    for i in range(0, len(time_str_list)):
        for j in range(i + 1, len(time_str_list)):
            time_period = time_str_list[i] + '-' + time_str_list[j]
            time_period_list.append(time_period)
            break

    return time_period_list


# 返回时间所属区间段, 区间段可自行设置时间间隔, 默认区间为60
# 如'2013-04-18 7:20:00' -> 7:00:00-8:00:00
def get_time_period(date_time, mins_delta=60):
    time_period_list = create_time_zone_range(mins_delta)
    time_str = date_time.split(' ')[1]
    period_return = ''
    for index, time_period in enumerate(time_period_list):
        st_time = time_period.split('-')[0]
        et_time = time_period.split('-')[1]
        lower_bound = time_to_sec(time_str) - time_to_sec(st_time)
        upper_bound = time_to_sec(et_time) - time_to_sec(time_str)

        if lower_bound >= 0 and upper_bound > 0:
            period_return = time_period_list[index]
        elif (lower_bound >= 0) and (upper_bound < 0):
            period_return = time_period_list[index]

    return period_return


# date_time: '2013-04-15 04:23:00'
# 把YYYY-MM-DD H:M:S 时间转换成秒
# def date_time_to_sec(date_time):
#     date_time = time.strptime(date_time, '%Y-%m-%d %H:%M:%S')
#     init_date = datetime.date(1970, 1, 1)
#     each_date = datetime.date(date_time.tm_year, date_time.tm_mon, date_time.tm_mday)
#     delta_days = each_date-init_date
#     date_time_sec = datetime.timedelta(delta_days.days,
#                                        hours=date_time.tm_hour,
#                                        minutes=date_time.tm_min,
#                                        seconds=date_time.tm_sec).total_seconds()
#     return date_time_sec

def date_time_to_sec(date_time):
    date_time = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    init_date = datetime.date(1970, 1, 1)
    each_date = datetime.date(date_time.year, date_time.month, date_time.day)
    delta_days = each_date - init_date
    date_time_sec = datetime.timedelta(delta_days.days,
                                       hours=date_time.hour,
                                       minutes=date_time.minute,
                                       seconds=date_time.second).total_seconds()
    return date_time_sec


# param:date_time:日期;i.e. '2014-01-15'
# output:秒
# def date_to_sec(date_time):
#     date_time = time.strptime(date_time, '%Y-%m-%d')
#     init_date = datetime.date(1970, 1, 1)
#     each_date = datetime.date(date_time.tm_year, date_time.tm_mon, date_time.tm_mday)
#     delta_days = each_date-init_date
#     date_time_sec = datetime.timedelta(delta_days.days).total_seconds()
#     return date_time_sec
def date_to_sec(date_time):
    date_time = datetime.datetime.strptime(date_time, '%Y-%m-%d')
    init_date = datetime.date(1970, 1, 1)
    each_date = datetime.date(date_time.year, date_time.month, date_time.day)
    delta_days = each_date - init_date
    date_time_sec = datetime.timedelta(delta_days.days).total_seconds()
    return date_time_sec


# param:sec:秒
# output:日期
def sec_to_date(sec, format='%Y-%m-%d'):
    return datetime.datetime.fromtimestamp(float(sec)).strftime(format)


# def mth_time_to_sec(date_time):
#     date_time = time.strptime(date_time, '%Y-%m')
#     init_date = datetime.date(1970, 1, 1)
#     each_date = datetime.date(date_time.tm_year, date_time.tm_mon, date_time.tm_mday)
#     delta_days = each_date-init_date
#     date_time_sec = datetime.timedelta(delta_days.days).total_seconds()
#     return date_time_sec

def mth_time_to_sec(date_time):
    date_time = datetime.datetime.strptime(date_time, '%Y-%m')
    init_date = datetime.date(1970, 1, 1)
    each_date = datetime.date(date_time.year, date_time.month, date_time.day)
    delta_days = each_date - init_date
    date_time_sec = datetime.timedelta(delta_days.days).total_seconds()
    return date_time_sec


# time_str: '04:23:00'
# 把HMS时间转换成秒
# def time_to_sec(time_str):
#     hms = time.strptime(time_str, '%H:%M:%S')
#     hms_sec = datetime.timedelta(hours=hms.tm_hour, minutes=hms.tm_min, seconds=hms.tm_sec).total_seconds()
#     return hms_sec

def time_to_sec(time_str):
    hms = datetime.datetime.strptime(time_str, '%H:%M:%S')
    hms_sec = datetime.timedelta(hours=hms.hour, minutes=hms.minute, seconds=hms.second).total_seconds()
    return hms_sec


# 两个时间相减得到的秒数
def date_time_span(date_time_1, date_time_2):
    spac_sec = date_time_to_sec(date_time_1) - date_time_to_sec(date_time_2)
    return spac_sec


# 两个时间相减得到的天数
def day_used(date_time_1, date_time_2):
    day_span_days = 0
    if date_time_1 and date_time_2:
        day_span_days = date_time_span(date_time_1, date_time_2) / float(3600 * 24)
        day_span_days = math.ceil(day_span_days)
        if day_span_days == 0:
            day_span_days = 1
    return int(day_span_days)


def mth_used(date_time_1, date_time_2):
    mth_span = 0
    if date_time_1 and date_time_2:
        mth_span = round((day_used(date_time_1, date_time_2) / float(30), 0))

    return int(mth_span)


# 输出按照顺序的set
def ordered_set_list(need_list):
    d = OrderedDict()
    for x in need_list:
        d[x] = True
    ordered_list = [i for i in d]
    return ordered_list


# 找出最早最晚时间
def find_span_trans_date(trans_date_list):
    if trans_date_list:
        _trans_date_list = [i for i in trans_date_list if (type(i) == str or type(i) == unicode)]
        _trans_date_list = [j for j in _trans_date_list if j != "1970-01-01 00:00:00"]
        temp_time = []

        if _trans_date_list:
            for each_trans_date in _trans_date_list:
                date_time_sec = date_time_to_sec(each_trans_date)
                temp_time.append((each_trans_date, date_time_sec))

            temp_date, tem_sec = zip(*temp_time)
            min_sec = min(tem_sec)
            max_sec = max(tem_sec)
            earlist_trans = temp_date[tem_sec.index(min_sec)]
            last_trans = temp_date[tem_sec.index(max_sec)]

            return earlist_trans, last_trans
        else:
            return '', ''
    else:
        return '', ''


# unix timestamp转datetime
def unix_timestamp_to_dt(ts, div=1000):
    m = time.localtime(1.0 * ts / div)
    ms = "%s-%s-%s %s:%s:%s" % (m.tm_year, m.tm_mon, m.tm_mday, m.tm_hour, m.tm_min, m.tm_sec)
    return get_dt(ms)


def utc_dt():
    x = datetime.datetime.now(tz=pytz.UTC)
    return x


# datetime转unix timestamp
def dt_to_unix_timestamp(dt):
    return int(time.mktime(dt.timetuple()) * 1000)


# @return: 当前的datetime时间戳
def now_utc():
    return datetime.datetime.now(tz)


def mth_between(st_mth, et_mth):
    mth_format = "%Y-%m"
    st_mth_dt = datetime.datetime.strptime(st_mth, mth_format)
    et_mth_dt = datetime.datetime.strptime(et_mth, mth_format)
    tgt_list = list(rrule(MONTHLY, dtstart=st_mth_dt).between(st_mth_dt, et_mth_dt, inc=True))
    full_mth_list = [mth_dt.strftime(mth_format) for mth_dt in tgt_list]
    return full_mth_list


def local2utc(local_st):
    """
    本地时间转UTC时间（-8:00）
    :param local_st: 本地时间， str类型
    :return: UTC时间， str类型
    """
    time_struct = time.mktime(datetime.datetime.strptime(local_st, "%Y-%m-%d %H:%M:%S").timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st.strftime("%Y-%m-%d %H:%M:%S")


def get_updt(utc_timestamp):
    """
    把utc timestamp 转换成UTC datetime

    :param utc_timestamp:
    :return: UTC datetime
    """
    _utc_dt = ""
    if utc_timestamp:
        _utc_dt = unix_timestamp_to_dt(utc_timestamp, div=1)

    return _utc_dt


def utc_dt_to_local_str(dt_utc):
    """
    UTC datetime转成本地时间

    :param dt_utc: UTC datetime类型
    :return: local datatime string
    """
    dt_str = ""
    if dt_utc:
        _tz = pytz.timezone(pytz.country_timezones('cn')[0])
        dt_tz = datetime.datetime(year=dt_utc.year, month=dt_utc.month, day=dt_utc.day, hour=dt_utc.hour,
                                  minute=dt_utc.minute, second=dt_utc.second, tzinfo=pytz.utc).astimezone(_tz)

        dt_str = dt_tz.strftime('%Y-%m-%d %H:%M:%S')

    return dt_str


def validate_time_format(date_text, format='%Y-%m-%d'):
    try:
        datetime.datetime.strptime(date_text, format)
        return True
    except:
        # raise ValueError("Incorrect data format, should be %s" % format)
        print "Incorrect data format, should be %s" % format
        return False


def dt_str_to_utc(dts="2016-02-23"):
    return  dt_to_unix_timestamp(get_date(dts))


if __name__ == "__main__":
    # print today_timestamp()
    # next_n_days_timestamp()
    # dt_to_unix_timestamp
    print dt_str_to_utc()

