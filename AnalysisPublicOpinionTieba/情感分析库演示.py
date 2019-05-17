from SentimentAnalysis import Analysis

content = "喜欢"

resultJson = Analysis.analysisJson(content)
print(type(resultJson))	#json格式
print(resultJson)
# print('positive_prob:',resultJson['items'][0]['positive_prob'])
# 所以记得用下面那种

resultDict = Analysis.analysisDict(content)
print(type(resultDict))	#dict格式
print(resultDict)
print('positive_prob:',resultDict['items'][0]['positive_prob'])