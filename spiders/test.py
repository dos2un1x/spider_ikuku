# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from handler import tools
import re

source = tools.ungzip_file('link_1e37b1faa6057996395484fc25d8ee0c.html')
print source
if source is not None:
    try:
        s = source.strip()
        s = s.replace('\t','').replace('\r','').replace(' ','')
        re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
        re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I) #Script
        re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I) #style
        re_br=re.compile('<br\s*?/?>') #处理换行
        re_comment=re.compile('<!--[^>]*-->') #HTML注释
        blank_line = re.compile('\n+') #处理空行
        s=re_cdata.sub('',s) #去掉CDATA
        s=re_script.sub('',s) #去掉SCRIPT
        s=re_style.sub('',s) #去掉style
        s=re_br.sub('\n',s) #将br转换为换行
        s=re_comment.sub('',s) #去掉HTML注释
        s=blank_line.sub('\n',s) #去掉多余的空行
        # print s
        p1 = re.compile("src=\"(.+?)\"class=\"attachment-list-thumbwp-post-image\"")
        url1 = p1.search(s)
        print 'url1 is : ' + url1.group(1)
        p2 = re.compile("loadsrc=\"(.+?)\"")
        urls = p2.findall(s)
        for url in urls:
            print url

    except Exception,e:
        print e
