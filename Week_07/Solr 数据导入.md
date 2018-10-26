# Solr的搭建和导入数据

本机环境：Windows 10（64-bit）, Solr-5.5.2，MySQL-8.0.12, JDK-1.8.1-171(已配置环境变量)

## 1.Solr的下载和安装

[Solr各版本下载地址](http:\\archive.apache.org\dist\lucene\solr\)

这里我们使用`Solr-5.5.2`版本，下载zip包，解压即完成安装。

## 2.Solr的运行

使用CMD命令行，进入 `${Solr_HOME}\bin ` 键入相应命令来启动Solr

| 操作         | 命令                       |
| ------------ | -------------------------- |
| 启动solr服务 | solr start                 |
| 关闭solr服务 | solr stop -all             |
| 重启solr服务 | solr restart -p [port]     |
| 创建solr核心 | solr create -c [core_name] |

键入启动Solr的命令，CMD输出：” **Started solr server on port 8983,happy searching!** “ 说明服务启动成功。

浏览器键入 ：http://localhost:8983 即可看到solr的界面

## 3.创建核心

核心可以理解为是一个管理你索引位置、索引方式、配置数据源等的一个地方即可。用下面的命令创建一个core

CMD中键入：`${SOLR_HOME}\solr-5.5.2\bin>solr create -c [new_core]`

在`${SOLR_HOME}\solr-5.5.2\server\solr\`目录下可以看到刚刚创建好的`new_coer`核心,在这个新创建的核心中需要配置的文件有`managed-schema`、`solrconfig.xml` 、`data-config.xml`

**以下对文件的编辑，建议使用 `Notepad++` 来编辑，注意不要随意修改文件的编码格式和后缀名**

+ #### `solrconfig.xml` 的配置

	打开`solrconfig.xml`，在这里我们配置一下数据的导入方式，在`solrconfig.xml`找到其他的`requestHandler` （使用`Notepad++`的查找功能来快速查找），把下面的配置复制到一起，便于以后管理。

	```xml
	<requestHandler name="/dataimport" class="org.apache.solr.handler.dataimport.DataImportHandler">
	  <lst name="defaults">
	    <str name="config">data-config.xml</str>
	  </lst>
	</requestHandler>
	```

+ **`data-config.xml` 的配置**
  然后在conf目录下生成一个`data-config.xml`的文件，来配置一下我们的数据源，指定一下数据库的链接地址和表中的数据即可。

  ```xml
  <dataConfig>
      <dataSource type="JdbcDataSource" driver="com.mysql.jdbc.Driver" url="jdbc:mysql://127.0.0.1:3306/test" user="root" password="password" batchSize="-1"/>
      <document>
          <entity name="solr_test" query="SELECT paper_id,name,author,unit,keywords,year FROM paper FROM solr_test">
              <field column="paper_id" name="id" />
  			<field column="name" name="name" />
  			<field column="author" name="author" />
  			<field column="unit" name="unit" />
  			<field column="keywords" name="keywords" />	
              <field column="year" name="year" />
          </entity>
      </document>
  </dataConfig>
  ```

  + `url="jdbc:mysql://127.0.0.1:3306/test"`是MySQL数据库的地址端口和数据库的名称
  + `user="root" password="password"` 填入MySQL用户名和对应密码 

+ #### managed-schema.xml的配置

	数据的来源配置解决了，选择来考虑一下对哪些数据进行索引。打开`managed-schema.xml`，把下面的配置添加上去，field的配置不细说了……

	```xml
	<field name="paper_id" type="int" indexed="true" stored="true" multiValued="false"/>
	    <field name="name" type="string" indexed="true" stored="true" multiValued="false"/>
	    <field name="author" type="string" indexed="true" stored="true" multiValued="false"/>
	    <field name="unit" type="string" indexed="true" stored="true" multiValued="false"/>
	    <field name="keywords" type="string" indexed="true" stored="true" multiValued="false"/>
	    <field name="year" type="int" indexed="true" stored="true" multiValued="false"/>
	<!--
	<copyField source="word" dest="defaultField" />
	<copyField source="keyNo" dest="defaultField" />
	-->
	```

+ **依赖的添加**

	将`${SOLR_HOME}\solr-5.5.2\dist`目录下的` solr-dataimporthandler-5.5.2.jar`还有`solr-dataimporthandler-extras-5.5.2.jar` 拷贝到
	`${SOLR_HOME}\solr-5.5.2\server\solr-webapp\webapp\WEB-INF\lib`中即可。

	除了上面的两个包以外，还需要导入`jdbc`的包，不然你会发现数据导入不进去。下载`jdbc`包，放到刚刚的文件夹`${SOLR_HOME}\solr-5.5.2\server\solr-webapp\webapp\WEB-INF\lib`中，那么数据来源这块就算解决了。

	**重启一下Solr服务**，在Solr界面中选择你创建的核心，点击`Dataimport`功能，选择`entity`, 然后执行即可。

## 4.可能遇到的问题：

+ 报错信息：

	`Can not find: admin-extra.menu-top.html `

	`Can not find: admin-extra.menu-bottom.html `

	`Can not find: admin-extra.html `

| Level | Core | Logger | Message |
| ---- | ----- | ---- | ---------------------- |
| ERROR | null | ShowFileRequestHandler | **Can not find: admin-extra.menu-top.html**[${Solr_HOME}\solr-5.5.2\server\solr\paper\conf\admin-extra.menu-top.html] |
| ERROR | null | ShowFileRequestHandler | **Can not find: admin-extra.menu-bottom.html**[${Solr_HOME}\solr\Environment\solr-5.5.2\server\solr\paper\conf\admin-extra.menu-bottom.html] |
| ERROR | null | ShowFileRequestHandler | **Can not find: admin-extra.html** [${Solr_HOME}\solr\Environment\solr-5.5.2\server\solr\paper\conf\admin-extra.html] |

+ 解决方案：
	+ 到`${SOLR_HOME}\example\example-DIH\solr\solr\conf`目录下将`admin-extra.xml`、`admin-extra.menu-bottom.html`和`admin-extra.menu-top.html`复制到`${SOLR.SOLR.HOME}\core2\conf`目录下

报错信息：

`The server time zone value ÖÐ¹ú±ê×¼Ê±¼ä' is unrecognized or represents more than one`

+ 解决办法，更改数据库时区，操作如下:
  + CMD进入`MySQL`的`bin`目录
  + 启动`MySQL` : `net start mysql`
  + 登陆数据库，如果数据库在本地，可以使用以下指令：`mysql -u root -p`
  + `set global time_zone="+8:00";`


