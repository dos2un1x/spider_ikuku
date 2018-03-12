# -*- coding:utf-8 -*-
import logging
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import config

cf = config.get_conf()


# selenium webdriver chrome 爬取页面url
def chrome_crawler(_url, _choose, _value):
    # 设置浏览器headless及不加载图片
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-javascript')
    chrome_options.add_argument('--disable-plugins')
    chrome_options.add_argument('--disable-extensions')
    # chrome_options.add_argument('--window-size=800,600')
    # chrome_options.add_extension('/home/spider/AdBlock_v3.24.0.crx')
    prefs = {'profile.default_content_setting_values': {'images': 2}}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--headless')
    # linux下配置
    # chrome_options.add_argument('--no-sandbox')
    # 是否动态代理IP
    # chrome_options.add_argument('--proxy-server=http://' + AutoProxy(url))
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # 隐式等待（可和显式一同使用，取大），推荐使用显式
    if cf.getboolean('web', 'time_out'):
        # driver.implicitly_wait(15)
        driver.set_script_timeout(cf.getint('web', 'script_time'))
        driver.set_page_load_timeout(cf.getint('web', 'page_load'))
    try:
        driver.get(_url)
        # 显式等待（0.5秒查询一次，查询5秒，共查询10次）
        # EC.presence_of_all_elements_located（复数形式，查到所有的通过）
        # EC.presence_of_element_located（单数）
        if cf.getboolean('web', 'driver_wait'):
            try:
                if _choose == 'byid':
                    WebDriverWait(driver, cf.getint('web', 'wait_time'), 0.5).until(
                        EC.presence_of_element_located((By.ID, _value)))
                elif _choose == 'byclass':
                    WebDriverWait(driver, cf.getint('web', 'wait_time'), 0.5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, _value)))
                else:
                    logging.info('please choose crawl conditions')
                return driver.page_source
            except TimeoutException:
                logging.info('WebDriverWait exception url is: ' + _url)
        else:
            return driver.page_source
    except WebDriverException, e:
        logging.info(e)
    finally:
        driver.quit()
