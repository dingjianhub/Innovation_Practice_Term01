# 百度贴吧情感分析

## 第一版

* 简单爬虫(返回所有结果字符串，带\<br\>与\<a\>的简单字符串(为了放在body里面))

* 简单的后端 GET 仅仅是加载前面的字符串

## 第二版

* 简单爬虫（返回列表，其中每一篇文章是字典）

* 情绪分析接口（传入content,自动请求返回json或dict）

* 仅爬取第一层（为了做舆情分析）得到字典，并且每篇文章加入情感结果

  ```json
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
  ```

# 版本三
* 针对只爬第一楼的情况又重新分析网页做了针对性的优化，极大提高了爬取速度，同时删去相对无用的"作者"信息，删去之前写的已经用不到的函数，减小代码体积