# -*- coding:utf-8 -*-
import logging
import urllib2
from handler import config
from handler import mysqldb
from handler import logger
from handler import redisdb
from handler import tools

cf = config.get_conf()
db = mysqldb.mysqldb()
rdb = redisdb.redisdb()
logger.set_log('spider_down.log')


def spider_down():
    try:
        get_url = rdb.consumers(cf.get('redis', 'down_queue'))
        headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        req = urllib2.Request(url=get_url, headers=headers)
        url = urllib2.urlopen(req, timeout=5)
        binary_data = url.read()
        filename = tools.get_md5(get_url) + '.jpg'
        status = tools.save_to_file(filename, binary_data)
        if status:
            logging.info('img download ok !')
        else:
            rdb.producers(cf.get('redis', 'down_queue'), get_url)
    except Exception, e:
        logging.info(e)
        rdb.producers(cf.get('redis', 'down_queue'), get_url)
    finally:
        url.close()

def main():
    while True:
        spider_down()

if __name__ == '__main__':
    logging.info('start spider')
    main()