# -*- coding:utf-8 -*-
import logging
import time

from handler import config
from handler import mysqldb
from handler import logger
from handler import redisdb
from handler import crawler_url
from handler import tools

cf = config.get_conf()
db = mysqldb.mysqldb()
rdb = redisdb.redisdb()
logger.set_log('spider_link.log')


def spider_link():
    try:
        url = rdb.consumers(cf.get('redis', 'link_queue'))
        if url is not None:
            logging.info('crawler url is: ' + url)
            page = crawler_url.chrome_crawler(url, '', '')
            if page is not None:
                page = page.encode('utf-8')
                filename = 'link_' + tools.get_md5(url) + '.html'
                logging.info(filename)
                status = tools.gzip_file(filename, page)
                if status:
                    rdb.producers(cf.get('redis', 'html_queue'), filename)
                else:
                    rdb.producers(cf.get('redis', 'link_queue'), url)
    except Exception, e:
        logging.info(e)
        rdb.producers(cf.get('redis', 'link_queue'), url)
    finally:
        time.sleep(1)


def main():
    while True:
        spider_link()


if __name__ == '__main__':
    logging.info('start spider')
    main()
