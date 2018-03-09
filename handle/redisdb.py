# coding=utf-8
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
            logging.info('redis connect error !')

    def producers(self, queue, url):
        try:
            rconn = self.connect_redis()
            # rconn.sadd(queue,url)
            rconn.lpush(queue, url)
        except Exception, e:
            logging.info(e)

    def consumers(self, queue):
        try:
            rconn = self.connect_redis()
            # url = rconn.spop(queue)
            url = rconn.blpop(queue, 0)[1]
            return url
        except Exception, e:
            logging.info(e)
