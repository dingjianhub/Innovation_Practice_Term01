"""
@author:BirdBirdLee
@time:2019/05/09
@note:应老师要求，只爬第一楼，并做情感分析，所以对传回字典进行格式修改
"""

from bs4 import BeautifulSoup
import requests
import re
import random
import json
import time
from urllib.parse import quote

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
}


def pause():
    '''
    延迟一到两秒
    '''
    sleepTime = random.randint(100, 2000) * 1.0 / 1000
    # 延迟0.1-2秒
    time.sleep(sleepTime)


def make_up_url(url_prefix, url_suffix, keyword):
    """
    组装url
    url_prefix:前缀
    url_suffix:后缀
    keyword:关键词
    网址用的是百分号编码
    """
    return url_prefix + quote(keyword) + url_suffix


def get_url_list_of_one_page(origin_url, page=0):
    """
    获取某页所有的链接
    拼装每一页实际网址并请求
    origin_url: 得到的网址
    page: 页数
    """
    # global originUrl
    # url = originUrl + str(page*50)
    url = origin_url + str(page + 1)
    html = requests.get(url, headers=headers)
    pattern = r'href="(/p/[0-9]*)[^ ]'
    # 获取每一页上所有文章的网址
    article_list = re.findall(pattern, html.text)

    for i in range(len(article_list)):
        article_list[i] = "http://tieba.baidu.com" + article_list[i]
    return article_list


def get_soup_of_article(article_url, page=1):
    """
    获取每一页soup对象
    """
    url = article_url + "?pn="
    html = requests.get(url + str(page), headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    return soup


def get_title(article):
    """
    获取标题
    随便哪页都能获取，选第一页
    """
    soup = get_soup_of_article(article, 1)
    title = soup.find(class_='core_title_txt')['title'].strip()
    return title


def get_main_content_first_floor_advance(article_soup):
    # 返回列表
    content_district = article_soup.find(class_="d_post_content_firstfloor")
    # 因为是第一楼这样子定位更精确更快
    content = content_district.find(class_=['d_post_content', 'j_d_post_content'])
    # 获得内容
    if (content != None):
        content = content.text.strip()
    else:
        content = ""
    # pause()
    time.sleep(0.2)
    return content


def get_list_first_floor_advance(page_want=1, keyword="杭州电子科技大学"):
    '''
    根据关键词和指定页数爬取
    page_want:爬搜索结果的几页
    keyword:关键词
    '''
    result = []
    url_prefix = "http://tieba.baidu.com/f/search/res?ie=utf-8&isnew=1&kw=&qw="
    url_suffix = "&un=&rn=10&pn=0&sd=&ed=&sm=1&only_thread=1&pn="
    origin_url = make_up_url(url_prefix, url_suffix, keyword)
    for page in range(page_want):  # 逐页爬取
        article_list = get_url_list_of_one_page(origin_url, page)
        for article in article_list:
            soup = get_soup_of_article(article)
            title = get_title(article)
            one_article_info_dict = {}
            one_article_info_dict['firstFloorContent'] = get_main_content_first_floor_advance(soup)
            one_article_info_dict['title'] = title
            one_article_info_dict['href'] = article
            # one_article_info_dict['positive_prob'] = 0
            # one_article_info_dict['confidence'] = 0
            # print(oneArticleDict)
            result.append(one_article_info_dict)
        print("page", page + 1, "process done")

    print("All first floor comment get done")
    return result


if __name__ == '__main__':
    print('开始爬取')

    result = get_list_first_floor_advance(2, "杭州电子科技大学 三位一体")

    for res in result:
        print(res['firstFloorContent'])
        print(res['title'])
        print(res['href'])
