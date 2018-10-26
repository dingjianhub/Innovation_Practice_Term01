#!/user/bin/python
# -*- coding: utf-8 -*-
"""
@author: yhj
@time: 2018/9/13 14:54
@desc: 
"""
from csv import DictWriter

from src.BaseReptile import BaseReptile
import csv


class PaperReptile(BaseReptile):
    """
    知网论文的解析
    """

    def __init__(self, url, model="get", params=None, **kwargs):
        BaseReptile.__init__(self, url)
        self.paperDic = dict()
        self.get_etree(model, params, **kwargs)

    def set_url(self, url, model="get", params=None, **kwargs):
        self.url = url
        self.get_etree(model, params, **kwargs)

    def parse_html(self):
        """
        解析并解析知网的论文网页，得到论文的名字，作者，摘要，关键字等信息
        :return: 返回论文的信息的字典
        """
        if self.tree is None or self.requestCode != 1:
            raise RuntimeError("%s页面解析失败" % self.url)
        papername = self.get_elements_info('//div[@id="mainArea"]//h2[@class="title"]//text()')
        authors = self.get_elements_info('//div[@class="author"]//a/text()')
        organization = self.get_elements_info('//div[@class="orgn"]//a/text()')
        abstract = self.get_elements_info('//span[@id="ChDivSummary"]//text()')
        catalogs = self.get_elements_info('//div[@class="wxBaseinfo"]/p')
        keywords = None;
        classification = None
        if catalogs is not None:  # 获取关键字和分类号
            for catalog in catalogs:
                label = catalog.xpath('./label/@id')
                label = label[0] if label else None
                if label == "catalog_KEYWORD":  # 判断该p标签下是关键字还是分类号
                    keywords = catalog.xpath('./a/text()')
                    if keywords:
                        keywords = "".join([n.strip() for n in keywords])
                    else:
                        keywords = None
                elif label == "catalog_ZTCLS":
                    classification = catalog.xpath('./text()')
                    classification = classification[0] if classification else None
        self.paperDic['name'] = self.list_to_str(papername)
        self.paperDic['authors'] = self.list_to_str(authors, ";")
        self.paperDic['organization'] = self.list_to_str(organization, ";")
        self.paperDic['keywords'] = keywords
        self.paperDic['abstract'] = self.list_to_str(abstract)
        self.paperDic['classification'] = classification
        self.show_paper_dict()
        # add
        # 以下为 dingjianhub 为实现数据持久化存储的代码
        # self.save_paper_dict_into_csv(r"..\resource\result.csv")
        # 用r防止被转义
        #end
        return self.paperDic

    def show_paper_dict(self):
        """
        显示获取的论文信息
        :return: 
        """
        for key in self.paperDic:
            print(key, self.paperDic[key])

    # add
    # 以下为 dingjianhub 为实现数据持久化存储的代码
    '''
    def save_paper_dict_into_csv(self, path=""):
        fieldnames = ['name', 'authors', 'organization',
                      'keywords', 'abstract', 'classification']  # 第一行的标头
        with open(path, 'a+', encoding='utf-8', newline='') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            # writer.writeheader()    # 写标头
            writer.writerow(self.paperDic)  # 一次写入一个字典
    #end
    '''
    @staticmethod
    def url_create(dbCode, filename):
        """
        根据dbcode和filename生成论文的url
        :param dbCode: 
        :param filename: 
        :return: 
        """
        return "http://kns.cnki.net/kcms/detail/detail.aspx?dbCode=%s&filename=%s" % (dbCode, filename)
