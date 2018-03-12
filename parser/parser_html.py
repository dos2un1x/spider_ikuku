# -*- coding:utf-8 -*-
import logging
import time
import re
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


def parser(html):
    source = tools.ungzip_file(html)
    if source is not None:
        try:
            s = source.strip()
            s = s.replace('\t', '').replace('\r', '').replace(' ', '')
            re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
            re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
            re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
            re_br = re.compile('<br\s*?/?>')  # 处理换行
            re_comment = re.compile('<!--[^>]*-->')  # HTML注释
            blank_line = re.compile('\n+')  # 处理空行
            s = re_cdata.sub('', s)  # 去掉CDATA
            s = re_script.sub('', s)  # 去掉SCRIPT
            s = re_style.sub('', s)  # 去掉style
            s = re_br.sub('\n', s)  # 将br转换为换行
            s = re_comment.sub('', s)  # 去掉HTML注释
            s = blank_line.sub('\n', s)  # 去掉多余的空行
            re_title = re.compile("<title>(.+?)<\/title>")
            title = re_title.search(s)
            logging.info(title.group(1))
            re_first = re.compile("src=\"(.+?)\"class=\"attachment-list-thumbwp-post-image\"")
            first = re_first.search(s)
            first_url = first.group(1)
            rdb.producers(cf.get('redis', 'down_queue'), first_url)
            re_urls = re.compile("loadsrc=\"(.+?)\"")
            urls = re_urls.findall(s)
            for url in urls:
                rdb.producers(cf.get('redis', 'down_queue'), url)
        except Exception, e:
            logging.info(e)
            rdb.producers(cf.get('redis', 'html_queue'), html)


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
            parser(html)
    except Exception, e:
        logging.info(e)
        rdb.producers(cf.get('redis', 'html_queue'), html)
    finally:
        time.sleep(1)


def main():
    while True:
        parser_html()


if __name__ == '__main__':
    logging.info('start parser htmls')
    main()
