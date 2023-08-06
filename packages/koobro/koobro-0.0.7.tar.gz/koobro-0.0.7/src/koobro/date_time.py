import datetime


def datetime_to_timestamp(dt: datetime.datetime, style=None):
    """
    datetime转时间戳

    示例：
    t = datetime.datetime(2012, 12, 12, 23, 59, 59, 48000)
    result = datetime_to_timestamp(t)       ->   1355327999.048 (float)
    result = datetime_to_timestamp(t, 10)   ->   1355327999 (int)
    result = datetime_to_timestamp(t, 13)   ->   1355327999048 (int)

    :param dt: 日期时间
    :param style: 时间戳类型
    :return:
    """

    if type:
        if str(style) == '10':
            return int(round(dt.timestamp()))

        if str(style) == '13':
            return int(round(dt.timestamp() * 1000))

    return dt.timestamp()


def timestamp_to_datetime(ts, tz=None) -> datetime.datetime:
    """
    时间戳转datetime

    :param ts: 时间戳
    :param tz: 时区。默认是本地
    :return:
    """
    if len(str(ts)) == 13:
        if tz == 'utc':
            return datetime.datetime.utcfromtimestamp(ts / 1000)
        return datetime.datetime.fromtimestamp(ts / 1000)
    if tz == 'utc':
        return datetime.datetime.utcfromtimestamp(ts)
    return datetime.datetime.fromtimestamp(ts)


def datetime_to_string(dt: datetime.datetime, style: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    datetime转字符串

    :param dt: 日期时间
    :param style: 转换格式
    :return:
    """
    if style == 'whole':
        return dt.strftime('%Y-%m-%d %H:%M:%S.%f')
    if style == 'date':
        return dt.strftime('%Y-%m-%d')
    if style == 'time':
        return dt.strftime('%H:%M:%S')
    else:
        return dt.strftime(style)


def string_to_datetime(s: str, style: str = None) -> datetime.datetime:
    """
    字符串转datetime

    示例：
    string_to_datetime('2022-02-11 13:44:01.48000')            ->   2022-02-11 13:44:01.480000
    string_to_datetime('2022-02-11 13:44:01')                  ->   2022-02-11 13:44:01
    string_to_datetime('2022-02-11')                           ->   2022-02-11 00:00:00
    string_to_datetime('2022-02-11 13:44:01.48000', '%Y-%m')   ->   2022-02-01 00:00:00

    :param s: 日期时间
    :param style: 转换格式
    :return:
    """
    s = s.strip()
    f = ''

    if style:
        f = style

    else:
        flag = False

        if len(s) == 10:
            f = '%Y-%m-%d'
            flag = True

        if len(s) == 19:
            f = '%Y-%m-%d %H:%M:%S'
            flag = True

        if '.' in s:
            f = '%Y-%m-%d %H:%M:%S.%f'
            flag = True

        if not flag:
            raise Exception('格式有误')

    return datetime.datetime.strptime(s, f)


def local_to_utc(dt: datetime.datetime) -> datetime.datetime:
    """
    本地时间转utc时间

    :param dt:
    :return:
    """
    return dt - datetime.timedelta(hours=8)


def utc_to_local(dt: datetime.datetime) -> datetime.datetime:
    """
    utc时间转本地时间

    :param dt:
    :return:
    """
    return dt + datetime.timedelta(hours=8)
