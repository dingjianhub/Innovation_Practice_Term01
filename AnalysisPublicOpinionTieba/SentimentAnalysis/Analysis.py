# coding=utf-8
import requests
import SentimentAnalysis.getAccessToken as gat
import json


def analysisJson(content=""):
    # 传入utf-8内容
    # 返回Json

    access_token = gat.get_access_token().strip()

    url_origin = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&'

    # url = url_origin + 'access_token='+access_token
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer?charset=UTF-8&access_token=" + access_token  # API

    headers = {
        'content-type': 'application/json',
    }

    text = {"text": content}

    analyze_response = requests.post(url=url, headers=headers, data=json.dumps(text).encode('utf-8'))
    # print(analyze_response.encoding)
    analyze_response.encoding = 'gbk'
    # 百度文档里面说请求编码是utf-8，传回来的就是utf-8
    # 但我请求utf-8传回来的是gbk
    j_analyze = analyze_response.text
    # 提取正文

    return j_analyze


def analysis_dict(content=""):
    # 传入utf-8内容
    # 返回字典

    access_token = gat.get_access_token().strip()

    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify&access_token=" + access_token  # API

    headers = {
        'content-type': 'application/json',
    }

    text = {"text": content}

    analyze_response = requests.post(url=url, headers=headers, data=json.dumps(text).encode('utf-8'))
    # print(analyze_response.encoding)
    analyze_response.encoding = 'utf-8'
    # 百度文档里面说请求编码是utf-8，传回来的就是utf-8
    # 但我请求utf-8传回来的是gbk
    d_analyze = json.loads(analyze_response.text)
    # 提取正文并把json转换成字典

    return d_analyze

res = analysis_dict("apple is great")
print(res)