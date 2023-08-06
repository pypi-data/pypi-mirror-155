# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/4/30 09:23
:LastEditTime: 2021/4/30 09:23
:LastEditors: SunYiTan
:Description: ID生成器，雪花算法
"""
import time
import threading


class InvalidSystemClock(Exception):
    """
    时钟回拨异常
    """
    pass


class IdWorker(object):
    """
    用于生成IDs
    """
    _lock = threading.Condition()

    # 64位ID的划分
    __WORKER_ID_BITS = 5
    __DATACENTER_ID_BITS = 5
    __SEQUENCE_BITS = 12

    # 最大取值计算
    __MAX_WORKER_ID = -1 ^ (-1 << __WORKER_ID_BITS)  # 2**5-1 0b11111
    __MAX_DATACENTER_ID = -1 ^ (-1 << __DATACENTER_ID_BITS)

    # 移位偏移计算
    __WORKER_ID_SHIFT = __SEQUENCE_BITS
    __DATACENTER_ID_SHIFT = __SEQUENCE_BITS + __WORKER_ID_BITS
    __TIMESTAMP_LEFT_SHIFT = __SEQUENCE_BITS + __WORKER_ID_BITS + __DATACENTER_ID_BITS

    # 序号循环掩码
    __SEQUENCE_MASK = -1 ^ (-1 << __SEQUENCE_BITS)

    # Twitter元年时间戳
    __TWEPOCH = 1288834974657

    __worker_id = 0
    __datacenter_id = 0
    __sequence = 0
    __last_timestamp = 0

    @classmethod
    def init(cls, datacenter_id, worker_id, sequence=0):
        """
        初始化
        :param datacenter_id: 数据中心（机器区域）ID
        :param worker_id: 机器ID
        :param sequence: 其实序号
        """
        # sanity check
        if worker_id > cls.__MAX_WORKER_ID or worker_id < 0:
            raise ValueError('worker_id值越界')

        if datacenter_id > cls.__MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError('datacenter_id值越界')

        cls.__worker_id = worker_id
        cls.__datacenter_id = datacenter_id
        cls.__sequence = sequence

        cls.__last_timestamp = -1  # 上次计算的时间戳

    @classmethod
    def get_id(cls):
        """
        获取新ID
        :return:
        """
        cls._lock.acquire()
        try:
            timestamp = cls._gen_timestamp()

            # 时钟回拨
            if timestamp < cls.__last_timestamp:
                error = 'clock is moving backwards. Rejecting requests until {}'.format(cls.__last_timestamp)
                raise InvalidSystemClock(error)

            if timestamp == cls.__last_timestamp:
                cls.__sequence = (cls.__sequence + 1) & cls.__SEQUENCE_MASK
                if cls.__sequence == 0:
                    timestamp = cls._til_next_millis(cls.__last_timestamp)
            else:
                cls.__sequence = 0

            cls.__last_timestamp = timestamp

            new_id = ((timestamp - cls.__TWEPOCH) << cls.__TIMESTAMP_LEFT_SHIFT) | (
                    cls.__datacenter_id << cls.__DATACENTER_ID_SHIFT) | \
                     (cls.__worker_id << cls.__WORKER_ID_SHIFT) | cls.__sequence
            return new_id

        except Exception as e:
            raise e
        finally:
            cls._lock.release()

    @classmethod
    def _gen_timestamp(cls):
        """
        生成整数时间戳
        :return:int timestamp
        """
        return int(time.time() * 1000)

    @classmethod
    def _til_next_millis(cls, last_timestamp):
        """
        等到下一毫秒
        """
        timestamp = cls._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = cls._gen_timestamp()
        return timestamp
