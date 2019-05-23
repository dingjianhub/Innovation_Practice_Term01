from flask import Flask, request, render_template

from flask_bootstrap import Bootstrap
# from flask.ext.bootstrap import Bootstrap

from tiebaSpider import tieba3, spiderOnlyFirstFloorAdvance
import json

app = Flask(__name__)  # 创建一个Web应用

bootstrap = Bootstrap(app)


# @app.route('/test')
# def test():
#     return render_template('test.html')

@app.route('/show', methods=['GET', 'POST'])  # 定义路由(Views)，可以理解为定义页面的URL
def show():
    # return "这是用Python + Flask 搞出来的。" # 渲染页面
    page = int(request.args.get('page'))
    keyword = request.args.get('keyword')
    # result = tieba3.gogogoStringBr(page, keyword)
    # return render_template('show.html', page=page, keyword=keyword, result=result)
    # return render_template('info.html', page=page, keyword=keyword, result=result)
    return render_template('info.html', page=page, keyword=keyword)


@app.route('/info', methods=['GET', 'POST'])  # 定义路由(Views)，可以理解为定义页面的URL
def info():
    page = int(request.args.get('page'))
    keyword = request.args.get('keyword')
    result = spiderOnlyFirstFloorAdvance.get_list_first_floor_advance(page_want=page, keyword=keyword)
    # for res in result:
    #     print(res['firstFloorContent'])
    #     print(res['title'])
    #     print(res['href'])
    result = json.dumps(result).encode('utf-8')
    return result


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)  # 运行，指定监听地址为 127.0.0.1:8080
    # tieba3.gogogoString(1, "杭州电子科技大学")
