import requests
import json
import urllib3
import sys
import zlib
import codecs
import time
import logging
import uuid


def get_access_token():
    '''
    鉴权认证机制
    '''
    headers = {'content-type': 'application/json'}
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    cilent_id = 'yV5uZkZWHg83KTt2Mwlmzt5z'
    client_secret = 'ryeGhbmZ69fFr84kMxjVTUYEEMcZtqsZ'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&' + 'client_id=' + cilent_id + '&' + 'client_secret=' + client_secret
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
            accessTokenResponse = requests.post(url=host, headers=headers)
            break
        except requests.exceptions.ConnectionError:
            print('ConnectionError -- please wait 3 seconds')
        except requests.exceptions.ChunkedEncodingError:
            print('ChunkedEncodingError -- please wait 3 seconds')
        except:
            if tries < (maxTryNum - 1):
                continue
            else:
                logging.error("Has tried %d times to access, all failed!", maxTryNum)
                break
    content = accessTokenResponse.text
    content = json.loads(content)  # 将access_token的json数据结构（字符串）转化为字典
    # print(content)
    if content:
        if "access_token" in content:
            return content["access_token"]
        else:
            return ""


'''接口接入，返回json格式数据'''


def get_content(text):
    access_token = get_access_token().strip()
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=" + access_token  # API
    headers = {"Content-Type": "application/json"}
    data = {"text": text}
    try:
        data = json.dumps(data, encoding="gbk", ensure_ascii=False).encode('gbk')
        r = requests.post(url, data=data, headers=headers)
        return r.text
    except Exception as e:
        print('a' + str(e))
        return 0


if __name__ == '__main__':
    path1 = 'contents.txt'  # 评论信息
    path2 = 'contents_emotion.txt'  # 评论情感信息
    files_emotion = open(path2, 'a', encoding='gbk')
    with open(path1, 'r', encoding='gbk') as files:
        comment = files.readline()
        uuid1 = uuid.uuid1()
        print(comment)
        # data = line[0].strip()
        result = get_content(comment.encode('gbk'))
        # print("the result is : " + str(result))
        # sleep_time = 2  # 设置睡眠时间，防止请求过快
        # time.sleep(sleep_time)
        result = str(result)
        result = json.loads(result)  # str转成dict
        if result.has_key('items'):
            # if 'items' in result:
            for i in range(len(result['items'])):
                if result['items'][i]['sentiment'] == 0:  # 判断感情极性
                    print(comment + '-----' + '消极观点')
                    files_emotion.write(str(uuid1) + '\t' + comment + '\t' + '0' + '\n')
                if result['items'][i]['sentiment'] == 1:
                    print(comment + '-----' + '中性观点')
                    files_emotion.write(str(uuid1) + '\t' + comment + '\t' + '0.5' + '\n')
                if result['items'][i]['sentiment'] == 2:
                    print(comment + '-----' + '积极观点')
                    files_emotion.write(str(uuid1) + '\t' + comment + '\t' + '1' + '\n')
        files_emotion.close()
