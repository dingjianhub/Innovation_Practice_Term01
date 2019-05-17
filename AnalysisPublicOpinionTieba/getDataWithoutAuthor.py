"""
@返回数据格式:
[{
		'firstFloorContent': '第一楼内容',
		'title': '标题',
		'href': 'http链接',
		'positive_prob': 积极性,
		'confidence': 可信度
	},

	{
		'firstFloorContent': '第一楼内容',
		'title': '标题',
		'href': 'http链接',
		'positive_prob': 积极性,
		'confidence': 可信度
	}
]
"""

from tiebaSpider import spiderOnlyFirstFloorAdvance as soff
from SentimentAnalysis import Analysis
import csv


def get_content_and_sentiment_dict(page=1, keyword="杭州电子科技大学"):
    article_list = soff.get_list_first_floor_advance(page, keyword)
    # 获取所有文章的信息的列表，每个数据元素格式如下
    '''
    {'firstFloorContent': '第一楼内容', 
    'title': '标题', 
    'href': 'http链接'
    }
    '''
    for article in article_list:
        # print(article)
        sentiment_dict = Analysis.analysis_dict(article['firstFloorContent'])
        print(sentiment_dict)
        # 对每篇文章第一楼内容进行情感分析
        # print(str(sentiment_dict['items'][0]['positive_prob']))
        # print(str(sentiment_dict['items'][0]['confidence']))
        # # 积极性概率存回字典
        article['positive_prob'] = sentiment_dict['items'][0]['positive_prob']
        # 积极性存回字典
        article['confidence'] = sentiment_dict['items'][0]['confidence']
    # print(article)
    return article_list


def get_comment_and_sentiment_dict_to_csv(page=1, keyword="杭州电子科技大学"):
    headers = ['authorName', 'firstFloorContent',
               'title', 'href', 'positive_prob', 'confidence']
    data_list = get_content_and_sentiment_dict(page=page, keyword=keyword)
    print("All contents with sentiment done")
    with open('20190427.csv', 'w') as f:
        print('saving')
        date_writer = csv.DictWriter(f, data_list[0].keys())
        date_writer.writeheader()
        for data in data_list:
            date_writer.writerow(data)
        print('save done')


if __name__ == '__main__':
    print("start")
    page = 1
    keyword = "杭州电子科技大学 三位一体"

    '''
    dataList = getContentAndSentimentDict(page = page, keyword = keyword)
    # print(dataList)
    print("All contents with sentiment done")
    for data in dataList:
        print(data)
    '''

    get_comment_and_sentiment_dict_to_csv(page=page, keyword=keyword)
