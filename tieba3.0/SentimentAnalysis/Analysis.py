# coding=utf-8
import requests
import SentimentAnalysis.getAccessToken as gat
import json
import uuid

def analysisJson(content=""):
    # 传入utf-8内容
    # 返回Json

    access_token = gat.get_access_token().strip()

    url_origin = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&'

    # url = url_origin + 'access_token='+access_token
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=" + access_token  # API

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


def analysisDict(content=""):
    # 传入utf-8内容
    # 返回字典

    access_token = gat.get_access_token().strip()

    url_origin = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&'

    # url = url_origin + 'access_token='+access_token
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=" + access_token  # API

    headers = {
        'content-type': 'application/json',
    }

    text = {"text": content}

    analyze_response = requests.post(url=url, headers=headers, data=json.dumps(text).encode('utf-8'))
    # print(analyze_response.encoding)
    analyze_response.encoding = 'gbk'
    # 百度文档里面说请求编码是utf-8，传回来的就是utf-8
    # 但我请求utf-8传回来的是gbk
    d_analyze = json.loads(analyze_response.text)
    # 提取正文并把Json转换成字典

    return d_analyze


if __name__ == '__main__':
    path1 = 'contents.txt'  # 评论信息
    path2 = 'contents_emotion.txt'  # 评论情感信息
    files_emotion = open(path2, 'a', encoding='utf-8')
    with open(path1, 'r', encoding='utf-8') as files:
        comments = files.readlines()
        for comment in comments:
            uuid1 = uuid.uuid1()
            print(comment)
            # data = line[0].strip()
            result = analysisDict(comment)
            # print("the result is : " + str(result))
            # sleep_time = 2  # 设置睡眠时间，防止请求过快
            # time.sleep(sleep_time)
            #if result.has_key('items'):
            if 'items' in result:
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
