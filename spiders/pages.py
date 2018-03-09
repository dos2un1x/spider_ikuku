# coding=utf-8
import logging

from bs4 import BeautifulSoup
from handle import config
from handle import mysqldb
from handle import logger
from handle import crawl_url
from handle import redisdb

cf = config.get_conf()
db = mysqldb.mysqldb()
rdb = redisdb.redisdb()
logger.set_log('pages.log')


def pages():
    try:
        page = crawl_url.handle_url(cf.get('web', 'start_url'), 'byclass', 'paged')
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
    logging.info('start pages spider')
    pages()
    logging.info('end pages spider')
