"""
@返回数据格式:
[{
		'authorName': '作者名',
		'firstFloorContent': '第一楼内容',
		'title': '标题',
		'href': 'http链接',
		'positive_prob': 积极性,
		'confidence': 可信度
	},
	{
		'authorName': '作者名',
		'firstFloorContent': '第一楼内容',
		'title': '标题',
		'href': 'http链接',
		'positive_prob': 积极性,
		'confidence': 可信度
	}
]
"""

# from tiebaSpider import spiderOnlyFirstFloor as soff
from tiebaSpider import spiderOnlyFirstFloorAdvance as soff
from SentimentAnalysis import Analysis
import csv


def get_content_and_sentiment_dict(page=1, keyword="杭州电子科技大学"):
    article_list = soff.gogogo_list_first_floor_advance(page, keyword)
    # 获取所有文章的信息的列表，每个数据元素格式如下
    '''
    {
    'firstFloorContent': '第一楼内容', 
    'title': '标题', 
    'href': 'http链接'}
    '''
    for article in article_list:
        sentimentDict = Analysis.analysisDict(article['firstFloorContent'])
        # 对每篇文章第一楼内容进行情感分析
        article['positive_prob'] = sentimentDict['items'][0]['positive_prob']
        # 积极性存回字典
        article['confidence'] = sentimentDict['items'][0]['confidence']
    # 积极性存回字典
    # print(article)
    return article_list


def getContentAndSentimentDictToCsv(page=1, keyword="杭州电子科技大学"):
    headers = ['authorName', 'firstFloorContent',
               'title', 'href', 'positive_prob', 'confidence']
    dataList = getContentAndSentimentDict(page=page, keyword=keyword)
    print("All contents with sentiment done")
    with open('20190427.csv', 'w') as f:
        print('saving')
        dWriter = csv.DictWriter(f, dataList[0].keys())
        dWriter.writeheader()
        for data in dataList:
            dWriter.writerow(data)
        print('save done')


if __name__ == '__main__':
    print("start")
    page = 1
    keyword = "杭州电子科技大学 三位一体"
    '''
    dataList = getContentAndSentimentDict(page = page, keyword = keyword)
    # print(dataList)
    for data in dataList:
        print(data)
    '''
    getContentAndSentimentDictToCsv(page=page, keyword=keyword)
