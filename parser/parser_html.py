# -*- coding:utf-8 -*-
import logging
import time
from bs4 import BeautifulSoup

from handler import config
from handler import mysqldb
from handler import logger
from handler import redisdb
from handler import tools

cf = config.get_conf()
db = mysqldb.mysqldb()
rdb = redisdb.redisdb()
logger.set_log('parser_html.log')

def parser_html():
    try:
        html = rdb.consumers(cf.get('redis', 'html_queue'))
        logging.info('html is: ' + html)
        if 'page_' in html:
            logging.info('parser page is: ' + html)
            page = tools.ungzip_file(html)
            soup = BeautifulSoup(page, 'lxml')
            urls = soup.find_all('a', class_='weibo_title')
            for url in urls:
                url = url['href']
                status = rdb.producers(cf.get('redis', 'link_queue'), url)
                if status is False:
                    rdb.producers(cf.get('redis', 'html_queue'), html)
        elif 'link_' in html:
            logging.info('parser link is: ' + html)
    except Exception, e:
        logging.info(e)
        rdb.producers(cf.get('redis', 'html_queue'), html)
    finally:
        time.sleep(1)


def main():
    while True:
        parser_html()


if __name__ == '__main__':
    logging.info('start parser html')
    main()
