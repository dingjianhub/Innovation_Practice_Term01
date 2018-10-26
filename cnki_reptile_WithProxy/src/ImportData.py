#!/user/bin/python
# -*- coding: utf-8 -*-
"""
@author: yhj
@time: 2018/10/14 13:19
@desc: 导入数据到数据库
"""

import codecs
from src.mysql import mysql_operate
''' 导入格式有部分问题代码
column_map = {u"期刊名称": "paper_name", u"年份": "year", u"期数": "issue", u"论文标题": "name", u"论文作者": "author",
              u"论文单位": "unit", u"论文关键字": "keywords", u"论文摘要": "abstract", u"论文分类号": "classification"}
'''
column_map = {u"论文标题": "name", u"论文作者": "author", u"论文单位": "unit", u"论文关键字": "keywords", u"论文摘要": "abstract",
              u"论文分类号": "classification", u"论文年份": "year"}

def insert_data(conn):
    cursor = conn.cursor()
    fp = codecs.open("../resource/result.txt", "r", encoding="utf-8")
    insert_data = dict()
    for line in fp:
        line = line.strip()  # 去掉换行等前后空白符
        if line == "":
            inser_sql = mysql_operate.add_sql("paper", **insert_data)
            cursor.execute(inser_sql)
            insert_data.clear()
        else:
            key, value = line.split(":", 1)
            if key == u"论文作者" or key == u"论文单位":
                value = value.split(";")[0]
            insert_data[column_map[key]] = value
    conn.commit()


def insert_expert(conn):
    cursor = conn.cursor()
    cursor.execute("insert into expert (name, unit) select author,unit from paper group by author, unit")
    conn.commit()

    # cursor = conn.cursor()
    # columns = ["author", "unit"]
    # expert_set = set()  # set去除重复的同单位下的同名的人
    # select_sql = mysql_operate.select_sql("paper", *columns)
    # cursor.execute(select_sql)
    # for author, unit in cursor.fetchall():
    #     if author + "\t" + unit not in expert_set:
    #         inser_sql = mysql_operate.add_sql("expert", name=author, unit=unit)
    #         cursor.execute(inser_sql)
    #         expert_set.add(author + "\t" + unit)
    # conn.commit()


def insert_join(conn):
    cursor = conn.cursor()
    cursor.execute("insert into paper_expert_join (expert_id, expert_name, paper_id, paper_name) "
                   "select expert_id, expert.name, paper_id, paper.name from paper "
                   "join expert on expert.name = paper.author and expert.unit = paper.unit")
    conn.commit()


if __name__ == '__main__':
    conn = mysql_operate.connection_sql("my_paper_database", host='127.0.0.1', user='root', passwd='password', port=3306, charset='utf8')
    insert_data(conn)
    insert_expert(conn)
    insert_join(conn)
    mysql_operate.close_sql(conn)