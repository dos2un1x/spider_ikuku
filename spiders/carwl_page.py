# coding=utf-8
import logging
import time

from handle import config
from handle import mysqldb
from handle import logger
from handle import redisdb
from handle import crawl_url
from handle import tools

cf = config.get_conf()
db = mysqldb.mysqldb()
rdb = redisdb.redisdb()
logger.set_log('carwl_page.log')


def carwl_page():
    while True:
        try:
            url = rdb.consumers(cf.get('redis', 'page_queue'))
            if url is not None:
                logging.info(url)
                page = crawl_url.handle_url(url, 'byclass', 'paged')
                if page is not None:
                    page = page.encode('utf-8')
                    # page = tools.gzip_data(page)
                    filename = tools.get_md5(url) + '.html'
                    logging.info(filename)
                    # status = tools.msg_pack(filename, page)
                    status = tools.gzip_file(filename, page)
                    if status is False:
                        rdb.producers(cf.get('redis', 'page_queue'), url)
            else:
                logging.info('no url')
        except Exception, e:
            logging.info(e)
            rdb.producers(cf.get('redis', 'page_queue'), url)
        finally:
            time.sleep(1)


if __name__ == '__main__':
    logging.info('start crawl page')
    carwl_page()
    logging.info('end crawl page')
