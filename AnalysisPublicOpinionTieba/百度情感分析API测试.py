#coding=utf-8
import requests
import SentimentAnalysis.getAccessToken as gat
import json

def analysis():
	# access_token = '24.3432770adcbc25a05a345a7722e20e39.2592000.1558228875.282335-16057417'
	access_token = gat.get_access_token().strip()

	url_origin = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&'

	#url = url_origin + 'access_token='+access_token
	url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token="+access_token  # API

	# print(url)

	headers = {
		'content-type': 'application/json',
	}

	text = {"text": "喜欢" }

	analyze_response = requests.post(url = url, headers=headers, data = json.dumps(text).encode('utf-8'))
	# print(analyze_response.encoding)
	analyze_response.encoding = 'gbk'
	# 百度文档里面说请求编码是utf-8，传回来的就是utf-8
	# 但我请求utf-8传回来的是gbk
	j_analyze = json.loads(analyze_response.text)
	print(j_analyze)
	print(j_analyze['text'])


