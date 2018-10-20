# Week_05  MySQL数据库

## 1.安装MySQL数据库

关于**MySQL**数据库的操作和学习，可以移步到**菜鸟教程**：[MySQL教程](https://www.runoob.com/mysql/mysql-tutorial.html)

## 2.数据库可视化工具：

+ **MySQL Workbench**（MySQL官方工具，免费使用）
+ **Navicat Premium**(付费工具，支持Mac平台)

## 3.数据库创建代码

```mysql
-- 创建论文表
CREATE TABLE IF NOT EXISTS `paper`(
	`paper_id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,		-- 论文id自动增长 
	`name` VARCHAR(255) NOT NULL,													-- 论文标题 
	`authors` VARCHAR(255),																-- 论文作者
	`unit` VARCHAR(255),																	-- 论文单位
	`keywords` VARCHAR(255),															-- 论文关键字
	`abstract` VARCHAR(255),															-- 论文摘要
	`classification` VARCHAR(255),											-- 论文分类号
	`year` INT,															-- 论文年份
	`issue` INT															-- 论文期号
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建专家表
CREATE TABLE IF NOT EXISTS `expert`(
	`expert_id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,	-- 专家id自动增长 
	`name` VARCHAR(255) NOT NULL,													-- 专家名字
	`unit` VARCHAR(255)																		-- 专家单位
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建论文和专家的关联表
CREATE TABLE IF NOT EXISTS `paper_expert_join`(
	`id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	`expert_id` INT,																		-- 专家id	
	`expert_name` VARCHAR(255),													-- 专家名字
	`paper_id` INT,																			-- 论文id
	`paper_name` VARCHAR(255),													-- 论文名字
	`expert_role` INT																		-- 专家在论文为几作
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

**数据库入库步骤：**

+ 创建论文表，专家表，关联表
+ `Python`连接数据库，将数据导入数据库
	+ `python3.x`需要`pymysql`可以在`Pycharm`中搜索安装或者`pip`直接安装

## 4.运行导入数据到数据库的`Python`程序