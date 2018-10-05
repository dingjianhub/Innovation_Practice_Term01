#!/user/bin/python
# -*- coding: utf-8 -*-
"""
@author: yhj
@time: 2018/9/13 10:01
@desc: 
"""
from src.BaseReptile import BaseReptile
import re


class PaperJournalReptile(BaseReptile):
    """
    知网期刊页面的解析
    """
    def __init__(self, url, model="get", params=None, **kwargs):
        super(PaperJournalReptile, self).__init__(url)
        self.get_etree(model, params, **kwargs)         # 请求页面，并将其交给lxml处理，将html形成文档树，方便使用xpath获取内容

    def parse_html(self):
        """
        获取并解析论文期刊页面，得到dbcode和filename中的内容
        :return: 
        """
        if self.tree is None or self.requestCode != 1:
            raise RuntimeError("%s页面解析失败" % self.url)
        if self.html.find("暂无目录信息") == -1:  # 找到该目录信息
            paperUrlInfo = list()
            hrefs = self.get_elements_info('//span[@class="name"]/a[@target="_blank"]/@href')  # 提取页面所有a标签下的href的内容
            if hrefs:
                for href in hrefs:
                    pattern = re.compile("dbCode=(.*?)&filename=(.*?)&")  # 利用正则表达式提取出dbCode和filename的内容
                    match = pattern.search(href)
                    if match and len(match.groups()) == 2:
                        paperUrlInfo.append([match.group(1), match.group(2)])
            return paperUrlInfo
        else:
            print("%s: 该页面暂无目录信息" % self.url)
            return None

    @staticmethod
    def url_create(year, issue, pykm, paperId):
        """
        根据期刊指定的信息生成请求期刊目录的url
        :param year: 期刊年份
        :param issue: 哪一期
        :param pykm: 期刊知网标识，可以在resource下的journalnameCodes.txt的第三个字段中查到
        :param paperId: 第几页目录 
        :return: 
        """
        url = "http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year=%d&issue=%02d&pykm=%s&pageIdx=%d" \
               % (year, issue, pykm, paperId)
        return url

