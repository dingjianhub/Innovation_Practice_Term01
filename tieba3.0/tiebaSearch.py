from flask import Flask,request,render_template
import flask
import tieba3

app = Flask(__name__) # 创建一个Web应用
 
@app.route('/show') # 定义路由(Views)，可以理解为定义页面的URL
def show(): 
    # return "这是用Python + Flask 搞出来的。" # 渲染页面
    page = int(request.args.get('page'))
    keyword = request.args.get('keyword')
    result = tieba3.gogogoStringBr(page, keyword)
    return render_template('show.html', page = page, keyword = keyword, result = result)
 
if __name__ == '__main__':
	app.run(host='127.0.0.1',port=8080) # 运行，指定监听地址为 127.0.0.1:8080
	# tieba3.gogogoString(1, "杭州电子科技大学")
