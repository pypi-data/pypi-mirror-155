# -*- coding: utf-8 -*-
# AUTHOR  : wjia
# TIME    : 2022/6/21 17:08
# FILE    : tool
# PROJECT : funfunc
# IDE     : PyCharm
from datetime import datetime as _datetime
import os
from functools import wraps
import time
from typing import List as _List
import logging


def get_current_str_time() -> str:
    now_time = _datetime.now()
    str_time = now_time.strftime('%Y年%m月%d日星期%w %H时%M分%S秒')
    return str_time


def download_file(url, save_path):
    import requests

    r = requests.get(url, stream=True)
    with open(os.path.join(save_path), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)


def time_it(method):
    @wraps(method)
    def waapper(*args, **kwargs):
        start = time.time()
        result = method(*args, **kwargs)
        end = time.time()
        print('{} USED TIME:{}'.format(method.__name__, end - start))

        return result

    return waapper


def quick_sort(arr: _List[int]) -> _List[int]:
    if len(arr) < 2:
        return arr
    temp = arr[0]
    small = [i for i in arr[1:] if i <= temp]
    big = [i for i in arr[1:] if i > temp]
    return quick_sort(small) + [temp] + quick_sort(big)


def get_basic_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger(__name__)
    return logger


def chunks(arr: list, n: int) -> list:
    """将列表n等分"""
    return [arr[i:i + n] for i in range(0, len(arr), n)]


def get_host_ip():
    """查询本机ip地址"""
    import socket

    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def time_to_timestamp(date):
    """时间转化为时间戳"""
    return _datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timestamp()


def second_to_strtime(second: int):
    """秒转化为分秒"""
    return time.strftime("%M:%S", time.gmtime(second))


