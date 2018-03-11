# -*- coding:utf-8 -*-
import logging
import redis
import config

cf = config.get_conf()


class redisdb:
    def connect_redis(self):
        try:
            dbpool = redis.ConnectionPool(host=cf.get('redis', 'rhost'), port=cf.getint('redis', 'rport'),
                                          db=cf.getint('redis', 'db'))
            rpool = redis.StrictRedis(connection_pool=dbpool)
            return rpool
        except Exception, e:
            logging.info(e)
            return False

    def producers(self, queue, url):
        try:
            rconn = self.connect_redis()
            rconn.lpush(queue, url)
            return True
        except Exception, e:
            logging.info(e)
            return False

    def consumers(self, queue):
        try:
            rconn = self.connect_redis()
            url = rconn.blpop(queue, 0)[1]
            return url
        except Exception, e:
            logging.info(e)
            return False
