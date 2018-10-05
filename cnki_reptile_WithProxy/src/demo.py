#!/user/bin/python
# -*- coding: utf-8 -*-
"""
@author: yhj
@time: 2018/9/13 9:59
@desc: 
"""
from src.PaperJournalReptile import PaperJournalReptile
from src.PaperReptile import PaperReptile
import time
from src.Proxy import Proxy
proxy = Proxy("http://tpv.daxiangdaili.com/ip/?tid=557133875098914&num=1&delay=5&filter=on") # 代理ip获取地址
proxies = None


def get_proxy():
    global proxy
    return proxy.get_proxy()


def get_paper_url_info(year, issue, pykm, paperId):
    """
    获取指定目录下的论文的dbcode和filename
    为获取论文做准备
    :param year: 期刊年份
    :param issue: 哪一期
    :param pykm: 期刊知网标识，可以在resource下的journalnameCodes.txt的第三个字段中查到
    :param paperId: 第几页目录
    :return: 
    """
    global proxies
    try_num = 0
    print("开始获取%s期刊 %s年 第%s期第%s页目录" % (pykm, year, issue, paperId))
    url = PaperJournalReptile.url_create(year, issue, pykm, paperId)
    while try_num < 3:
        try:
            return PaperJournalReptile(url, proxies=proxies, timeout=5).parse_html()
        except Exception as e:
            proxies = get_proxy()
            try_num = try_num + 1


def get_paper_info(dbcode, filename):
    """
    解析论文页面，将论文的信息放在一个字典内
    :param dbcode: 
    :param filename: 
    :return: 
    """
    global proxies
    # proxies = get_proxy()
    try_num = 0
    url = PaperReptile.url_create(dbcode, filename)
    while try_num < 3:
        try:
            return PaperReptile(url, proxies=proxies, timeout=5).parse_html()
        except Exception as e:
            proxies = get_proxy()
            try_num = try_num + 1


if __name__ == '__main__':
    for dbcode, filename in get_paper_url_info(2018, 4, "HXDY", 0):
        print("=====================================================")
        get_paper_info(dbcode, filename)
        print("=====================================================\n")
        time.sleep(3) # 防止频繁访问造成IP被禁，采用简单的访问一次等待一段时间
