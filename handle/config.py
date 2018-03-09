# coding=utf-8
import ConfigParser
import logging


def get_conf():
    try:
        conf = ConfigParser.ConfigParser()
        conf.read('../conf/config.ini')
        return conf
    except Exception, e:
        logging.info(e)
