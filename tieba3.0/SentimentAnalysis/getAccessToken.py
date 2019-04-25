#coding=utf-8
import requests
import json
import logging

def get_access_token():

	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
		'content-type': 'application/json',
	}
	# client_id 为官网获取的AK， client_secret 为官网获取的SK
	cilent_id = 'yV5uZkZWHg83KTt2Mwlmzt5z'
	client_secret = 'ryeGhbmZ69fFr84kMxjVTUYEEMcZtqsZ'
	host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&'+'client_id='+cilent_id+'&'+'client_secret='+client_secret
	# print(host)
	# host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=xiP0z86PE3vNbXj9rfys22t0&client_secret=dPG8rmm9wjcApShdQlz7UPOYuI17Ozs0 '
	maxTryNum = 10
	for tries in range(maxTryNum):
		try:
			'''
			request = urllib2.Request(host)
			request.add_header('Content-Type', 'application/json; charset=utf-8')
			response = urllib2.urlopen(request)
			'''
			accessTokenResponse = requests.post(url = host, headers = headers)
			break
		except requests.exceptions.ConnectionError:
			print('ConnectionError -- please wait 3 seconds')
		except requests.exceptions.ChunkedEncodingError:
			print('ChunkedEncodingError -- please wait 3 seconds')
		except:
			if tries < (maxTryNum-1):
				continue
			else:
				logging.error("Has tried %d times to access, all failed!",maxTryNum)
				break
	content = accessTokenResponse.text
	content=json.loads(content) #将access_token的json数据结构（字符串）转化为字典
	# print(content)
	if content:
		if "access_token" in content:
			return content["access_token"]
		else:
			return ""

if __name__ == "__main__":
	access_token = get_access_token()
	print(access_token)