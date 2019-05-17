"""
@author:BirdBirdLee
@time:2019/03/08
"""

from bs4 import BeautifulSoup
import requests
import re
import time
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
	sleepTime = random.randint(100,2000)*1.0/1000
	# 延迟0.1-2秒
	time.sleep(sleepTime)

def make_up_url(urlPrefix, urlSuffix, keyWord):
	'''
	组装url
	urlPrefix:前缀
	urlPrefix:后缀
	keyWord:关键词
	'''
	return urlPrefix + quote(keyWord) + urlSuffix
	# 网址用的是百分号编码

def get_url_list_of_one_page(originUrl, page = 0):
	'''
	获取某页所有的链接
	originUrl: 得到的网址
	page: 页数
	'''

	# global originUrl
	# url = originUrl + str(page*50)
	# 拼装每一页实际网址并请求
	# 这是1.0请求网页的网址
	url = originUrl +str(page + 1)
	content = requests.get(url, headers = headers)
	pattern = r'href="(/p/[0-9]*)[^ ]'
	# 获取每一页上所有文章的网址
	articleList = re.findall(pattern, content.text)

	'''
	for article in articleList:
		article = "http://tieba.baidu.com"+article
		print(article)
	'''
	# 这种形式无法改变列表的值

	for i in range(len(articleList)):
		articleList[i] = "http://tieba.baidu.com" + articleList[i]
	return articleList

def get_soup_of_article(article, page=1):
	'''
	获取每一页soup对象
	'''
	url =  article + "?pn="
	htmlText = requests.get(url+str(page), headers=headers)
	soup = BeautifulSoup(htmlText.text, 'lxml')
	return soup

def get_max_page(article):
	'''
	获取最大页数
	随便找一页都可以获取，所以这里选第一页
	'''
	soup = get_soup_of_article(article, 1)
	pageMax = int(soup.find(class_="l_reply_num").find_all(class_="red")[1].text)
	return pageMax

def get_title(article):
	'''
	获取标题
	随便哪页都能获取，选第一页
	'''
	soup = get_soup_of_article(article, 1)
	title = soup.find(class_='core_title_txt')['title'].strip()
	return title

def get_main_content_soup_list(soup):
	classList = ["l_post", "j_l_post", "l_post_bright"]
	# classList = "div.l_post.j_l_post.l_post_bright"
	mainContents = soup.find_all("div",class_ = classList)
	# mainContents = soup.select(classList)
	return mainContents

def get_user_info_json(mainContent):
	# print(mainContent)
	print(type(mainContent))
	for key in mainContent.attrs:
		print(key)
	userInfo = mainContent.attrs['data-field']
	# print(mainContent)
	userInfoJson = json.loads(userInfo)
	userInfoDump = json.dumps(userInfoJson, sort_keys=True, indent=4, separators=(',', ': '))
	# 先用Loads把字符串解析成json然后用dumps格式化易于观察
	# print(userInfoDump)
	# date = userInfoJson['content']['date']
	# print(date)
	return userInfoJson

def get_date(userInfoJson):
	date = userInfoJson['content'].get('date', '日期未定义')
	# print(json.dumps(userInfoJson, sort_keys=True, indent=4, separators=(',', ': ')))
	return date

def get_main_contents(mainContents, pageMax = 1):

	floorIndex = 1
	for page in range(1,pageMax+1):
		floorsContent = mainContents
		for floorContent in floorsContent:
			print(floorIndex,"楼",end=" ")
			# f.write(str(floorIndex)+" 楼 ")
			authorName = floorContent.find(class_="d_name").text.strip()
			# 获得作者名称并去空格
			print(authorName," : ", end = "")
			# f.write(authorName+" : ")
			contentDistrict = floorContent.find(class_="d_post_content_main")
			# print(contentDistrict)
			content = contentDistrict.find(class_="clearfix")
			# 获得内容
			if(content != None):
				content = content.text.strip()
			else:
				content = "我是广告君"
				# 如果属性是空说明是广告
			print(content, end = '\n')
			# f.write(content+'\n')
			floorIndex+=1

			pause()
	print()

def get_main_contents_string(mainContents, pageMax = 1):

	result = ""
	floorIndex = 1
	for page in range(1,pageMax+1):
		floorsContent = mainContents
		for floorContent in floorsContent:
			# print(floorIndex,"楼",end=" ")
			result += str(floorIndex)+"楼 "
			# f.write(str(floorIndex)+" 楼 ")
			authorName = floorContent.find(class_="d_name").text.strip()
			# 获得作者名称并去空格
			# print(authorName," : ", end = "")
			result += authorName + " : "
			# f.write(authorName+" : ")
			contentDistrict = floorContent.find(class_="d_post_content_main")
			# print(contentDistrict)
			content = contentDistrict.find(class_="clearfix")
			# 获得内容
			if(content != None):
				content = content.text.strip()
			else:
				content = "我是广告君"
				# 如果属性是空说明是广告
			# print(content, end = '\n')
			result += content + "\n"
			# f.write(content+'\n')
			floorIndex+=1

			pause()
	result += "\n"
	return result

def get_main_contents_list(mainContents, pageMax = 1):
		# 返回列表
		# 每个子数据是个字典, 形如
		# {floorIndex:1, authorName:'name',floorContent: 'content'}

	result = []
	floorIndex = 1
	for page in range(1,pageMax+1):
		floorsContent = mainContents
		for floorContent in floorsContent:
			oneFloorContent = {}
			oneFloorContent['floorIndex'] = floorIndex
			# 楼层号
			authorName = floorContent.find(class_="d_name").text.strip()
			# 获得作者名称并去空格
			oneFloorContent['authorName'] = authorName
			contentDistrict = floorContent.find(class_="d_post_content_main")
			content = contentDistrict.find(class_="clearfix")
			# 获得内容
			if(content != None):
				content = content.text.strip()
			else:
				content = "我是广告君"
				# 如果属性是空说明是广告
			oneFloorContent['floorContent'] = content
			result.append(oneFloorContent)
			# print(oneFloorContent)
			floorIndex+=1

			pause()
	return result

def get_main_contents_string_br(mainContents, pageMax = 1):

	result = ""
	floorIndex = 1
	for page in range(1,pageMax+1):
		floorsContent = mainContents
		for floorContent in floorsContent:
			# print(floorIndex,"楼",end=" ")
			result += str(floorIndex)+"楼 "
			# f.write(str(floorIndex)+" 楼 ")
			authorName = floorContent.find(class_="d_name").text.strip()
			# 获得作者名称并去空格
			# print(authorName," : ", end = "")
			result += authorName + " : "
			# f.write(authorName+" : ")
			contentDistrict = floorContent.find(class_="d_post_content_main")
			# print(contentDistrict)
			content = contentDistrict.find(class_="clearfix")
			# 获得内容
			if(content != None):
				content = content.text.strip()
			else:
				content = "我是广告君"
				# 如果属性是空说明是广告
			# print(content, end = '\n')
			result += content + "<br/>"
			# f.write(content+'\n')
			floorIndex+=1

			pause()
	result += "<br/>"
	return result

def get_one_article(article):
	'''
	原先的爬取一篇文章，已重构

	'''

	# fileName = article[25:]+".txt" # 用文章链接作为文件名
	url =  article + "?pn="

	htmlText = requests.get(url+"1", headers=headers)
	# 先爬第一页获取总页数
	# print(content.text)
	htmlText = requests.get(url+"1", headers=headers)
	# print(htmlText.text)
	soup = BeautifulSoup(htmlText.text, 'lxml')
	pageMax = int(soup.find(class_="l_reply_num").find_all(class_="red")[1].text)
	# print(pageMax)
	title = soup.find(class_='core_title_txt')['title'].strip()


	fileName = 'articles_version2/'+article[3:]+'_'+title+'.txt'
	floorIndex = 1 #楼层
	with open(fileName, 'w', encoding='utf-8') as f:
		print('标题:',title)
		f.write('标题:'+title+'\n')
		for page in range(1,pageMax+1):

			htmlText = requests.get(url+str(page), headers=headers)
			soup = BeautifulSoup(htmlText.text, 'lxml')
			soup = BeautifulSoup(htmlText.text, 'lxml')
			# print(soup)
			floorsContent = soup.find_all(class_="l_post_bright")
			# floorsContent = soup.find_all(class_="d_post_content_main")
			# 获得存放所有楼层信息的标签
			# print(floors)
			for floorContent in floorsContent:
				# print(floorIndex,"楼",end=" ")
				f.write(str(floorIndex)+" 楼 ")
				authorName = floorContent.find(class_="d_name").text.strip()
				# 获得作者名称并去空格
				# print(authorName," : ", end = "")
				f.write(authorName+" : ")
				contentDistrict = floorContent.find(class_="d_post_content_main")
				# print(contentDistrict)
				content = contentDistrict.find(class_="clearfix")
				# 获得内容
				if(content != None):
					content = content.text.strip()
				else:
					content = "我是广告君"
					# 如果属性是空说明是广告
				# print(content, end = '\n')
				f.write(content+'\n')
				
				'''
				tailTest = contentDistrict.find(class_=["core_reply", "j_lzl_wrapper"])
				print(tailTest)
				tail = contentDistrict.find(class_=["core_reply", "j_lzl_wrapper"]).find_all('li')

				deployFloor = tail[0].text.strip()
				deployTime = tail[1].text.strip()

				print("楼层:",deployFloor, "发布时间:",deployTime)
				
				'''
				floorIndex+=1

				pause()
		# print()
			
def gogogo(pageWant = 1, keyWord = "杭州电子科技大学"):
	'''
	根据关键词和指定页数爬取
	pageWant:爬搜索结果的几页
	keyWord:关键词
	'''
	urlPrefix = "http://tieba.baidu.com/f/search/res?ie=utf-8&isnew=1&kw=&qw="
	urlSuffix = "&un=&rn=10&pn=0&sd=&ed=&sm=1&only_thread=1&pn="
	originUrl = make_up_url(urlPrefix, urlSuffix, keyWord)
	print(originUrl)
	for page in range(pageWant):
		articleList = get_url_list_of_one_page(originUrl, page)
		for article in articleList:
			soup = get_soup_of_article(article)
			pageMax = get_max_page(article)
			title = get_title(article)
			print("标题:",title)
			print("具体链接:",article)
			mainContentSoup = get_main_content_soup_list(soup)
			get_main_contents(mainContentSoup)

def gogogoString(pageWant = 1, keyWord = "杭州电子科技大学"):
	'''
	根据关键词和指定页数爬取
	pageWant:爬搜索结果的几页
	keyWord:关键词
	'''
	result = ""
	urlPrefix = "http://tieba.baidu.com/f/search/res?ie=utf-8&isnew=1&kw=&qw="
	urlSuffix = "&un=&rn=10&pn=0&sd=&ed=&sm=1&only_thread=1&pn="
	originUrl = make_up_url(urlPrefix, urlSuffix, keyWord)
	print(originUrl)
	for page in range(pageWant):
		articleList = get_url_list_of_one_page(originUrl, page)
		for article in articleList:
			soup = get_soup_of_article(article)
			pageMax = get_max_page(article)
			title = get_title(article)
			# print("标题:",title)
			result += "标题: "+title+"\n"
			# print("具体链接:",article)
			result += "具体链接: "+article+"\n"
			mainContentSoup = get_main_content_soup_list(soup)
			result += get_main_contents_string(mainContentSoup)

	return result

def gogogoStringBr(pageWant = 1, keyWord = "杭州电子科技大学"):
	'''
	根据关键词和指定页数爬取
	pageWant:爬搜索结果的几页
	keyWord:关键词
	'''
	result = ""
	urlPrefix = "http://tieba.baidu.com/f/search/res?ie=utf-8&isnew=1&kw=&qw="
	urlSuffix = "&un=&rn=10&pn=0&sd=&ed=&sm=1&only_thread=1&pn="
	originUrl = make_up_url(urlPrefix, urlSuffix, keyWord)
	print(originUrl)
	for page in range(pageWant):
		articleList = get_url_list_of_one_page(originUrl, page)
		for article in articleList:
			soup = get_soup_of_article(article)
			pageMax = get_max_page(article)
			title = get_title(article)
			# print("标题:",title)
			result += '标题: <a href="'+article+'">'+title+'</a> <br/>'
			# print("具体链接:",article)
			# result += "具体链接: "+article+"<br/>"
			# 加<a>使得能够点击
			mainContentSoup = get_main_content_soup_list(soup)
			result += get_main_contents_string_br(mainContentSoup)

	return result

def gogogoList(pageWant = 1, keyWord = "杭州电子科技大学"):
	'''
	根据关键词和指定页数爬取
	pageWant:爬搜索结果的几页
	keyWord:关键词
	'''
	result = []
	urlPrefix = "http://tieba.baidu.com/f/search/res?ie=utf-8&isnew=1&kw=&qw="
	urlSuffix = "&un=&rn=10&pn=0&sd=&ed=&sm=1&only_thread=1&pn="
	originUrl = make_up_url(urlPrefix, urlSuffix, keyWord)
	print(originUrl)
	for page in range(pageWant):
		articleList = get_url_list_of_one_page(originUrl, page)
		for article in articleList:
			soup = get_soup_of_article(article)
			pageMax = get_max_page(article)
			title = get_title(article)
			# print("标题:",title)
			oneArticleDict = {}
			# result += "标题: "+title+"\n"
			# print("具体链接:",article)
			# result += "具体链接: "+article+"\n"
			oneArticleDict['title'] = title
			oneArticleDict['href'] = article
			mainContentSoup = get_main_content_soup_list(soup)
			content = get_main_contents_list(mainContentSoup)
			oneArticleDict['content'] = content
			result.append(content)
			print(result)

	return result
# originUrl = "http://tieba.baidu.com/f?kw=%E6%9D%AD%E5%B7%9E%E7%94%B5%E5%AD%90%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6&ie=utf-8&pn="
# originUrl = "http://tieba.baidu.com/f/search/res?isnew=1&kw=&qw=%BA%BC%D6%DD%B5%E7%D7%D3%BF%C6%BC%BC%B4%F3%D1%A7&un=&rn=10&pn=0&sd=&ed=&sm=1&only_thread=1&pn="


if __name__ == '__main__':

	print('开始爬取')
	'''
	for page in range(5):
		articleList = get_url_list_of_one_page(page)
		for r in articleList:
			get_one_article(r)
			pause()
	'''

	# gogogo(1, "杭州电子科技大学")
	# 第一个参数是爬几页文章
	# 第二个参数是关键词

	result = gogogoList(1, "杭州电子科技大学")
	print(result)




	'''
	al = get_url_list_of_one_page(0)
	#print(al)
	soup = get_soup_of_article(al[0])
	print(al[0])
	mainContents = get_main_content_soup_list(soup)
	for mainContent in mainContents:
		#print(mainContent)
		userInfoJson = get_user_info_json(mainContent)
		# print(json.dumps(userInfoJson, sort_keys=True, indent=4, separators=(',', ': ')))
		date = get_date(userInfoJson)
		print(date)
	'''
	

