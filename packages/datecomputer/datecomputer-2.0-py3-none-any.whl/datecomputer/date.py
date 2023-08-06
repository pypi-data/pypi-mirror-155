
# encoding: utf-8
"""时间计算器"""

import time
import datetime
import calendar
from dateutil.relativedelta import relativedelta


def day(date: [str, datetime] = datetime.datetime.now()) -> int:
    """
    获取当前日
    """
    if not isinstance(date, (str, datetime.datetime)):
        raise TypeError("时间传入类型错误, 当前只允许字符串类型和datetime类型数据")
    if isinstance(date, str):
        date = strftime_to_datetime(date, "%Y-%m-%d")
    return date.day


def month(date: [str, datetime] = datetime.datetime.now()) -> int:
    """
    获取当前月份
    """
    if not isinstance(date, (str, datetime.datetime)):
        raise TypeError("时间传入类型错误, 当前只允许字符串类型和datetime类型数据")
    if isinstance(date, str):
        date = strftime_to_datetime(date, "%Y-%m-%d")
    return date.month


def year(date: [str, datetime] = datetime.datetime.now()) -> int:
    """
    获取年
    """
    if not isinstance(date, (str, datetime.datetime)):
        raise TypeError("时间传入类型错误, 当前只允许字符串类型和datetime类型数据")
    if isinstance(date, str):
        date = strftime_to_datetime(date, "%Y-%m-%d")
    return date.year


def datetime_to_strftime(date_time: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    datetime转换为字符串
    fmt: 返回的时间字符串格式
    """
    return date_time.strftime(fmt)


def strftime_to_datetime(date: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """
    时间字符串转datetime
    fmt: 传入的时间字符串格式
    """
    return datetime.datetime.strptime(date, fmt)


def timestamp_to_strftime(timestamp: int, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    时间戳转日期字符串: 1533952277 如果长度超过10位, 则取前十位数字
    """

    if len(str(timestamp)) < 10 or "." in str(timestamp)[:10]:
        return "时间戳不合法"

    time_array = time.localtime(int(str(timestamp)[:10]))
    return time.strftime(fmt, time_array)


def utc_to_date(utc_time: str, time_type=None, fmt: str = '%Y-%m-%d %H:%M:%S') -> [datetime, str]:
    """
    utc时间字符串转换为普通日期字符串
    utc_time: 如 '2022-03-31T11:25:29.910133+08:00'
    time_type: 希望转换成的格式，当前支持datetime和str, True: datetime, False: str
    fmt: 时间格式
    """
    td = datetime.datetime.fromisoformat(utc_time)
    return td if time_type else td.strftime(fmt)


def get_today_date(time_type: bool = False, fmt: str = "%Y-%m-%d %H:%M:%S") -> [datetime, str]:
    """
    获取今天的日期
    time_type: 返回的时间类型，为真则返回datetime, datetime不需要指定格式fmt; 为假返回str, 需要指定格式fmt
    fmt: 时间类型格式
    """
    if time_type:
        return datetime.datetime.now()
    else:
        return str(datetime.datetime.now().strftime(fmt))


def get_n_day_before(
        days: int, date_time: [datetime, str] = datetime.datetime.now(), time_type: bool = False) -> [datetime, str]:
    """
    date_time: 指定的时间点
    获取前days天的日期
    time_type: True：datetime, False: str
    """
    if isinstance(date_time, str):
        date_time = strftime_to_datetime(date_time, '%Y-%m-%d')
    delta = datetime.timedelta(days=days)
    days_before = date_time - delta
    return days_before if time_type else days_before.strftime('%Y-%m-%d')


def get_n_day_after(
        days: int, date_time: [datetime, str] = datetime.datetime.now(), time_type: bool = False) -> [datetime, str]:
    """
    获取后days天的日期
    time_type: True：datetime, False: str
    """
    if isinstance(date_time, str):
        date_time = strftime_to_datetime(date_time, '%Y-%m-%d')
    delta = datetime.timedelta(days=days)
    days_after = date_time + delta
    return days_after if time_type else days_after.strftime('%Y-%m-%d')


def get_n_month_before(
        months: int, date_time: [str, datetime] = datetime.datetime.now(), time_type: bool = False) -> [datetime, str]:
    """
    获取months月前的日期
    time_type: True：datetime, False: str
    """
    if isinstance(date_time, str):
        date_time = strftime_to_datetime(date_time, "%Y-%m-%d")
    return date_time - relativedelta(months=months) if time_type else \
        (date_time - relativedelta(months=months)).strftime("%Y-%m-%d")


def get_n_month_after(
        months: int, date_time: [str, datetime] = datetime.datetime.now(), time_type: bool = False) -> [datetime, str]:
    """
    获取months月后的日期
    time_type: True：datetime, False: str
    """
    if isinstance(date_time, str):
        date_time = strftime_to_datetime(date_time, "%Y-%m-%d")
    return date_time + relativedelta(months=months) if time_type else \
        (date_time + relativedelta(months=months)).strftime("%Y-%m-%d")


def is_leap(years: int) -> bool:
    """
    闰年判断
    是闰年返回True, 否则返回False
    """
    return calendar.isleap(years)
