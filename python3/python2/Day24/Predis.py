""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/12 16:11
# @Author  : iByte

# !/usr/bin/env python
# -*- coding:utf8 -*-

import redis


def get_pool(cls, redis_host, redis_port, redis_db):
    """build a redis connection
    :returns: a valid connection

    """
    try:
        pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_db)
        return redis.Redis(connection_pool=pool)
    except Exception as e:
        raise


if __name__ == '__main__':
    pool = get_pool("192.168.50.23", "6379", 9)
    conn = redis.Redis(connection_pool=pool)

    conn.set('key', 'Hello World')
    print(conn.get('key'))
    a = input('按任意键结束')
