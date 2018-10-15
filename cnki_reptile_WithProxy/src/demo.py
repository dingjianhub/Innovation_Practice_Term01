#!/user/bin/python
# -*- coding: utf-8 -*-
"""
@author: yhj
@time: 2018/9/13 9:59
@desc: 
"""
from typing import List, Any, Union

from src.PaperJournalReptile import PaperJournalReptile
from src.PaperReptile import PaperReptile
import time
import csv
import codecs
from src.Proxy import Proxy

proxy = Proxy("http://tpv.daxiangdaili.com/ip/?tid=557133875098914&num=1&delay=5&filter=on")  # 代理ip获取地址
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
            return PaperJournalReptile(url, proxies=proxies, timeout=5).parse_html
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
    # 以下为 dingjianhub 关于实现数据持久化存储的代码
    count = 0
    with open(r'..\resource\WantedInfo.txt', 'r') as file:
        count = len(file.readlines())
    i = 0

    keys = [('name', '论文标题'), ('authors', '论文作者'), ('organization', '论文单位'), ('keywords', '论文关键字'),
            ('abstract', '论文摘要'), ('classification', '论文分类号')]

    with open("../resource/result.txt", 'w') as fp:
        while i < count:
            # print("现在i的值为: " + str(i) + " , count的值为" + str(count))
            for line in open(r'..\resource\WantedInfo.txt', 'r').readlines():
                temp = line.split(',')
                pykm = temp[0]
                begin_year = temp[1]
                end_year = temp[2]
                begin_issue = temp[3]
                end_issue = temp[4]
                year = int(begin_year)
                while year <= int(end_year):
                    issue = int(begin_issue)
                    try:
                        while issue <= int(end_issue):
                            for dbcode, filename in get_paper_url_info(int(year), int(issue), str(pykm), 0):
                                print("=====================================================")
                                result = get_paper_info(dbcode, filename)
                                # fp.write("当前count的值为: " + str(i) + "\n")  # 调试用语句
                                # print("当前期数: " + str(issue))
                                fp.write("期刊名称: " + str(pykm) + "\n")
                                fp.write("年份: " + str(year) + "\n")
                                fp.write("期数: " + str(issue) + "\n")
                                for key, name in keys:
                                    fp.write(str(name) + ": " + str(result[key]))
                                    fp.write("\n")
                                fp.write("\n")
                                print("=====================================================\n")
                                time.sleep(0.3)  # 防止频繁访问造成IP被禁，采用简单的访问一次等待一段时间
                            issue = issue + 1
                    except Exception as e:
                        # issue = issue + 1
                        year = year + 1
            i = i + 1

''' yhj 关于数据持久化存储的代码(源码)

keys = [('name', '论文标题'), ('authors', '论文作者'), ('organization', '论文单位'), ('keywords', '论文关键字'),
        ('abstract', '论文摘要'), ('classification', '论文分类号')]
with open("../resource/result.txt", 'w') as fp:
    for dbcode, filename in get_paper_url_info(2018, 4, "HXDY", 0):
        print("=====================================================")
        result = get_paper_info(dbcode, filename)
        for key, name in keys:
            fp.write(name + ": " + result[key])
            fp.write("\n")
        fp.write("\n")
        print("=====================================================\n")
        time.sleep(3)  # 防止频繁访问造成IP被禁，采用简单的访问一次等待一段时间
'''
