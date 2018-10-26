# MySQL 使用

启动输入以下命令即可：

```sql
net start mysql
```

当 MySQL 服务已经运行时, 我们可以通过 MySQL 自带的客户端工具登录到 MySQL 数据库中, 首先打开命令提示符, 输入以下格式的命名:

```
mysql -h 主机名 -u 用户名 -p
```

如果我们要登录本机的 MySQL 数据库，只需要输入以下命令即可：

```
mysql -u root -p
```

按回车确认, 如果安装正确且 MySQL 正在运行, 会得到以下响应:

```
Enter password:
```

然后命令提示符会一直以 mysq> 加一个闪烁的光标等待命令的输入, 输入 **exit** 或 **quit** 退出登录。

