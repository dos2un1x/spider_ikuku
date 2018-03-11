# -*- coding:utf-8 -*-
import logging
import config


def set_log(filename):
    try:
        cf = config.get_conf()
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(filename=cf.get('log', 'logpath') + filename, level=logging.INFO, format=log_format,
                            filemode='a')
    except Exception, e:
        logging.info(e)
