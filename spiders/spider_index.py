# -*- coding:utf-8 -*-
import logging

from bs4 import BeautifulSoup
from handler import config
from handler import mysqldb
from handler import logger
from handler import crawler_url
from handler import redisdb

cf = config.get_conf()
db = mysqldb.mysqldb()
rdb = redisdb.redisdb()
logger.set_log('spider_index.log')


def spider_index():
    try:
        page = crawler_url.chrome_crawler(cf.get('web', 'start_url'), 'byclass', 'paged')
        if page is not None:
            soup = BeautifulSoup(page, 'lxml')
            urls = soup.find('div', class_='paged')
            for url in urls.find_all('a'):
                url = url['href']
                logging.info(url)
                rdb.producers(cf.get('redis', 'page_queue'), url)
    except Exception, e:
        logging.info(e)


if __name__ == '__main__':
    logging.info('start spider index')
    spider_index()
    logging.info('end spider index')
