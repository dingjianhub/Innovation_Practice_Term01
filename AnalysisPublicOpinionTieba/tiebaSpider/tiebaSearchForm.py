from flask import Flask,request,render_template
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import DataRequired
import tieba3

class TiebaForm(FlaskForm):
    keyword = StringField(label='搜索关键词',validators=[DataRequired("请输入关键词")],description="请输入关键词",render_kw={"required":"required"})
    page = StringField(label='筛选前几页',validators=[DataRequired("请输入页数")],description="请输入页数",render_kw={"required":"required"})
   
    submit = SubmitField('搜索')


app = Flask(__name__) # 创建一个Web应用

@app.route('/show') # 定义路由(Views)，可以理解为定义页面的URL
def show(): 
    # return "这是用Python + Flask 搞出来的。" # 渲染页面
    page = int(request.args.get('page'))
    keyword = request.args.get('keyword')
    result = tieba3.gogogoStringBr(page, keyword)
    return render_template('show.html', page = page, keyword = keyword, result = result)

@app.route('search',methods=("GET","POST"))
def add():
    form = NewsForm()
    if form.validate_on_submit():   # 如果form表单以submit进行提交，且用户填写的字段通过validators验证器，那么条件为真（submit提交方式就是“POST”）
        new_obj = News(             # 使用flask-sqlalchemy定义的一个表结构 
            page = form.page.data,
            keyword = form.keyword.data,
        )
        # db.session.add(new_obj)
        # db.session.commit()
        # 文字提示 flash
        # return redirect(url_for('admin',page=2))         # 跳转到admin页
    return render_template('showForm.html',form=form)

if __name__ == '__main__':
	app.run(host='127.0.0.1',port=8080) # 运行，指定监听地址为 127.0.0.1:8080
	# tieba3.gogogoString(1, "杭州电子科技大学")
