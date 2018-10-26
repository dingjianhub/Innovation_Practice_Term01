#!/user/bin/python
# -*- coding: utf-8 -*-


import pymysql

def connection_sql(db, host='127.0.0.1', user='root', passwd='root', port=3306, charset='utf8'):
    """
    连接数据库 
    """
    print('连接数据库 %s ...' % db)
    try:
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        print('连接成功')
        return conn
    except pymysql.Error as e:
        print('连接数据库失败 ',)
        print('Error :%s,%s' % (e.args[0], e.args[1]))
        return None


def close_sql(conn):
    print('关闭数据库...')
    try:
        conn.close()
        print('关闭数据库成功')
    except pymysql.Error as e:
        print('关闭数据库失败 ',)
        print('Error :%s,%s' % (e.args[0], e.args[1]))


def get_cursor(conn):
    return conn.cursor()


def get_count(cur, table):
    """
    得到表的总数量
    :param cur: 
    :param table: 
    :return: 
    """
    sql = "select count(id) from %s" % table
    cur.execute(sql)
    result = cur.fetchall()
    print('表%s一共有%d条数据' % (table, result[0][0]))
    return result[0][0]


def execute(cur, sql_str):
    return cur.execute(sql_str)


def commit(conn):
    conn.commit()


def execute_and_commit(conn, cur, *args):
    try:
        for sql_str in args:
            execute(cur, sql_str)
        commit(conn)
    except Exception as e:
        print("execute and commit catch a prolem")
        conn.rollback()


def add_sql(table, **kwargs):
    """
    数据库插入 
    :param table: 插入的表单的名字
    :param kwargs: 插入的字段名 = 插入的值
    :return: 
    example: add_sql(conn.cursor(), 'paper_total_04_24', id=1, unit='浙江', organization='杭电')
    """
    columns = ''
    values = ''
    for key in kwargs:
        columns = columns + '%s,' % key
        if isinstance(kwargs[key], str):
            values = values + "'%s'," % kwargs[key]
        else:
            values = values + '%s,' % kwargs[key]
    columns = columns[:-1]
    values = values[:-1]
    sql_str = 'insert into %s (%s) values (%s)' % (table, columns, values)
    print('[SQL]  %s' % sql_str)
    return sql_str


def select_sql(table, *args, **kwargs):
    """
    数据库查询
    :param table: 查询的表单
    :param args: 查询的字段
    :param kwargs: where=where语句  limit=limit语句  group by=group by语句
    :return: 
    :example: select_sql(conn.cursor(), 'paper_total_04_24', limit="0,100", where="id=12343 ", group_by="unit,name")
    """
    where_str = ''
    limit_str = ''
    group_str = ''
    for key in kwargs:
        if key == 'where':
            where_str = 'where %s' % kwargs[key]
        if key == 'limit':
            limit_str = 'limit %s' % kwargs[key]
        if key == 'group_by':
            group_str = 'group by %s' % kwargs[key]
    column_total = ''
    if args:
        for column in args:
            column_total = column_total + '%s,' % column
        column_total = column_total[:-1]
    else:
        column_total = '*'
    sql_str = "select %s from %s %s %s %s" % (column_total, table, where_str, group_str, limit_str)
    print('[SQL]  %s' % sql_str)
    return sql_str


def update_sql(table, where=None, **kwargs):
    """
    数据库更新字段
    :param cur: 
    :param table: 更新的表单
    :param where: where=where语句
    :param kwargs: column=update value
    :return:
    :example: a = {'id': 2, 'he': 's'};update_sql(conn.cursor(), 'paper_total_04_24', where="id = '1'", **a)
    """
    if where:
        where_str = 'where %s' % where
    else:
        where_str = ''
    if kwargs:
        set_str = ''
    else:
        print('没有需要更新的的字段')
        return
    for key in kwargs:
        if isinstance(kwargs[key], str):
            set_str = set_str + "%s='%s'," % (key, kwargs[key])
        else:
            set_str = set_str + '%s=%s,' % (key, kwargs[key])
    set_str = set_str[:-1]
    sql_str = "update %s set %s %s" % (table, set_str, where_str)
    print('[SQL]  %s' % sql_str)
    return sql_str


def copy_table_set(conn, new_table, old_table, *args):
    """
    数据库的去重操作(group_by默认时是复制表单)
    :param cur: 
    :param new_table: 创建的新表单（存放去重后的数据）
    :param old_table: 需要去重的表单
    :param args: 根据这些字段去重
    :return: 
    """
    print("===开始对%s表进行去重，得到新表%s===" % (old_table, new_table))
    cur = get_cursor(conn)
    copy_table_struct = "create table %s like %s" % (new_table, old_table)
    print(copy_table_struct)
    cur.execute(copy_table_struct)
    if args:
        column_total = ''
        for column in args:
            column_total = column_total + '%s,' % column
        copy_table_str = "insert into %s select * from %s group by %s" % (new_table, old_table, column_total)
    else:
        copy_table_str = "insert into %s select * from %s " % (new_table, old_table)
    print('[SQL]  %s' % copy_table_str)
    # return copy_table_str
    cur.execute(copy_table_str)
    conn.commit()
    print("===对%s表去重完成，得到新表%s" % (old_table, new_table))


def integration_tables(conn, new_table, db, *old_tables):
    """
    将多张表整合到一张表上（这几张表的字段格式要一致）
    :param cur: 
    :param new_table: 
    :param old_tables: 
    :return: 
    """
    print("===开始整合表%s，得到新表%s===" % (','.join(old_tables), new_table))
    cur = get_cursor(conn)
    for old_table in old_tables:
        sql_str = "select COLUMN_NAME from information_schema.COLUMNS " \
                  "where table_name = '%s' and table_schema = '%s'" % (old_table, db)
        print(sql_str)
        cur.execute(sql_str)
        columns = [items[0] for items in cur.fetchall() if 'id' not in items]
        print(columns)
        select_sql_str = select_sql(cur, old_table, *columns)
        sql_str = "insert into %s %s" % (new_table, select_sql_str)
        print('[SQL]  %s' % sql_str)
        cur.execute(sql_str)
        conn.commit()
    print("===整合表%s完成，得到新表%s===" % (','.join(old_tables), new_table))
