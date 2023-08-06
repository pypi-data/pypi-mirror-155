# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2020/7/21 10:50
:LastEditTime: 2020/7/21 10:50
:LastEditors: SunYiTan
:Description: redis工具类
"""

import redis
import time
import uuid
import math

from seven_framework import config


class RedisUtil(object):

    def __init__(self):
        if not hasattr(RedisUtil, 'pool'):
            # 创建redis连接池
            RedisUtil.get_redis_pool()
        self.conn = redis.Redis(connection_pool=RedisUtil.pool)

    @staticmethod
    def get_redis_pool():
        host = config.get_value("redis")["host"]
        port = config.get_value("redis")["port"]
        db = config.get_value("redis")["db"]
        password = config.get_value("redis")["password"]
        RedisUtil.pool = redis.ConnectionPool(host=host, password=password,
                                              port=port, db=db, decode_responses=True)

    #################################### str ######################################

    def set(self, key, value, time=None):
        # 非空即真非0即真
        if time:
            res = self.conn.setex(key, time, value)
        else:
            res = self.conn.set(key, value)
        return res

    def get(self, key):
        res = self.conn.get(key)
        if res:
            res = res
        return res

    def delete(self, key):
        return self.conn.delete(key)

    def incr(self, key, amount=1):
        return self.conn.incr(key, amount)

    #################################### hash ######################################

    def hset(self, name, key, value):
        return self.conn.hset(name, key, value)

    def hsetnx(self, name, key, value):
        return self.conn.hsetnx(name, key, value)

    def expire(self, name, time):
        return self.conn.expire(name, time)

    def hget(self, name, key=None):
        # 判断key是否我为空，不为空，获取指定name内的某个key的value; 为空则获取name对应的所有value
        if key:
            res = self.conn.hget(name, key)
        else:
            res = self.conn.hgetall(name)
        return res

    def hdel(self, name, key):
        return self.conn.hdel(name, key)

    def hincrby(self, name, key, amount=1):
        return self.conn.hincrby(name, key, amount)

    def hexists(self, name, key):
        return self.conn.hexists(name, key)

    def hvals(self, name):
        return self.conn.hvals(name)

    def hkeys(self, name):
        return self.conn.hkeys(name)

    #################################### 列表 ######################################

    def lpush(self, key: str, value: str, max_num: int):
        """
        :description: 列表，lpush方法，保留一定条数
        :last_editors: SunYiTan
        """
        self.conn.lpush(key, value)
        if max_num:
            self.conn.ltrim(key, 0, max_num - 1)

    def lindex(self, key: str, index: int) -> str:
        """
        :description: 列表，lindex方法
        :last_editors: SunYiTan
        """
        return self.conn.lindex(key, index)

    def lrange(self, key: str, start: int, stop: int):
        """
        :description: 列表，lrange方法
        :last_editors: SunYiTan
        """
        return self.conn.lrange(key, start, stop)

    def llen(self, key: str):
        """
        :description: 列表，llen方法
        :last_editors: SunYiTan
        """
        return self.conn.llen(key)

    #################################### 有序集合 ######################################

    def zadd(self, key: str, score: int, member: str, max_rank: int):
        """
        :description: 有序集合，zadd方法，保留一定条数
        :last_editors: SunYiTan
        """
        self.conn.zadd(key, {member: score})
        self.conn.zremrangebyrank(key, 0, -max_rank)

    def zrem(self, key: str, member: str):
        """
        :description: 有序集合，zrem方法
        :last_editors: SunYiTan
        """
        self.conn.zrem(key, member)

    def zrevrank(self, key: str, member: str) -> int:
        """
        :description: 有序集合，zrevrank方法
        :last_editors: SunYiTan
        """
        return self.conn.zrevrank(key, member)

    def zscore(self, key: str, member: str):
        """
        :description: 有序集合，zscore方法。返回有序集 key 中，成员 member 的 score 值。
        :last_editors: SunYiTan
        """
        return self.conn.zscore(key, member)

    def zrevrangeWithScores(self, key: str, min: int, max: int):
        """
        :description: 有序集合，zrevrangeWithScores方法
        :last_editors: SunYiTan
        """
        return self.conn.zrevrange(key, min, max, withscores=True)

    #################################### 分布式锁 ######################################

    def acquire_lock_with_timeout(self, lock_name, acquire_timeout=10, lock_timeout=9):
        """ 基于 Redis 实现的分布式锁

        :param lock_name: 锁的名称
        :param acquire_timeout: 获取锁的超时时间，默认 10 秒
        :param lock_timeout: 锁的超时时间，默认 9 秒
        :return:
        """

        identifier = str(uuid.uuid4())
        lockname = f'lock:{lock_name}'
        lock_timeout = int(math.ceil(lock_timeout))
        end = time.time() + acquire_timeout

        while time.time() < end:
            # 如果不存在这个锁则加锁并设置过期时间，避免死锁
            if self.conn.set(lockname, identifier, ex=lock_timeout, nx=True):
                return identifier

            time.sleep(0.001)

        return None

    def release_lock(self, lock_name, identifier):
        """ 释放锁

        :param conn: Redis 连接
        :param lockname: 锁的名称
        :param identifier: 锁的标识
        :return:
        """

        unlock_script = """
        if redis.call("get",KEYS[1]) == ARGV[1] then
            return redis.call("del",KEYS[1])
        else
            return 0
        end
        """
        lockname = f'lock:{lock_name}'
        unlock = self.conn.register_script(unlock_script)
        result = unlock(keys=[lockname], args=[identifier])
        if result:
            return True
        else:
            return False

    def can_pass_token_bucket(self, key, current_time, interval_per_token, max_token=10, init_token=10):
        """
        限流，令牌桶法
        :param key:
        :param current_time: 当前请求时间 ms
        :param interval_per_token: 每个令牌之间的间隔
        :param max_token: 桶内最大的令牌数量
        :param init_token: 初始的令牌数量
        :return:
        """
        limit_script = """
            local key = KEYS[1]
            local currentTime = tonumber(ARGV[1])
            local intervalPerToken = tonumber(ARGV[2])
            local maxToken = tonumber(ARGV[3])
            local initToken = tonumber(ARGV[4])
            local maxInterval = tonumber(ARGV[5])
            local tokens
            local bucket = redis.call("hmget", key, "lastTime", "lastToken")
            local lastTime = bucket[1]
            local lastToken = bucket[2]
            if lastTime == false or lastToken == false then
                tokens = initToken
                lastTime = currentTime
            else
                local thisInterval = currentTime - lastTime
                if thisInterval > 0 then
                    local tokensToAdd = math.floor(thisInterval / intervalPerToken)
                    tokens = math.min(lastToken + tokensToAdd, maxToken)
                    lastTime = lastTime + intervalPerToken * tokensToAdd
                else
                    tokens = lastToken
                    lastTime = lastTime
                end
            end
            if tokens == 0 then
                redis.call('hmset', key, 'lastToken', tokens, "lastTime", lastTime)
                redis.call('expire', key, 60 * 60)
                return false
            else
                redis.call('hmset', key, 'lastToken', tokens - 1, "lastTime", lastTime)
                redis.call('expire', key, 60 * 60)
                return true
            end
            """
        limit_key = f'limit:{key}'
        can_pass = self.conn.register_script(limit_script)
        return can_pass(keys=[limit_key], args=[current_time, interval_per_token, max_token, init_token])
