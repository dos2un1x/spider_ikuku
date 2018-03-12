# -*- coding:utf-8 -*-
import config
import hashlib
import logging
import msgpack
import StringIO
import gzip

cf = config.get_conf()
path = cf.get('web', 'html_path')


def save_to_file(file_name, contents):
    try:
        fh = open(path + file_name, 'wb')
        fh.write(contents)
        fh.flush()
        fh.close()
        return True
    except Exception, e:
        logging.info(e)
        return False


def read_to_file(file_name):
    try:
        fh = open(path + file_name, 'rb')
        contents = fh.read()
        fh.close()
        return contents
    except Exception, e:
        logging.info(e)
        return False


def get_md5(contents):
    try:
        md5 = hashlib.md5()
        md5.update(contents)
        md5 = md5.hexdigest()
        return md5
    except Exception, e:
        logging.info(e)


def msg_pack(file_name, contents):
    try:
        with open(path + file_name, 'wb') as f:
            msgpack.dump(contents, f)
    except Exception, e:
        logging.info(e)
        return False


def msg_unpack(file_name):
    try:
        with open(path + file_name, 'rb') as f:
            contents = msgpack.load(f)
            return contents
    except Exception, e:
        logging.info(e)
        return False


# gzip压缩数据流
def gzip_data(data):
    buf = StringIO.StringIO()
    f = gzip.GzipFile(mode='wb', fileobj=buf)
    try:
        f.write(data)
    finally:
        f.close()
    return buf.getvalue()


# gzip解压数据流
def ungzip_data(data):
    buf = StringIO.StringIO(data)
    f = gzip.GzipFile(mode='rb', fileobj=buf)
    try:
        r_data = f.read()
    finally:
        f.close()
    return r_data


# gzip压缩文件
def gzip_file(filename, data):
    f = gzip.open(path + filename, 'wb')
    try:
        f.write(data)
        return True
    except Exception, e:
        logging.info(e)
        return False
    finally:
        f.close()


# gzip解压文件
def ungzip_file(filename):
    f = gzip.open(path + filename, 'rb')
    try:
        r_data = f.read()
    finally:
        f.close()
    return r_data
