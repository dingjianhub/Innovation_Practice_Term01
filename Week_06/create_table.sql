-- 创建论文表
CREATE TABLE IF NOT EXISTS `paper`(
	`paper_id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,		-- 论文id自动增长 
	`name` VARCHAR(255) NOT NULL,													-- 论文标题 
	`author` VARCHAR(255),																-- 论文作者
	`unit` VARCHAR(255),																	-- 论文单位
	`keywords` VARCHAR(255),															-- 论文关键字
	`abstract` VARCHAR(1024),															-- 论文摘要
	`classification` VARCHAR(255),												-- 论文分类号
	`year` INT																						-- 论文年份
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
	`paper_name` VARCHAR(255)													-- 论文名字
)ENGINE=InnoDB DEFAULT CHARSET=utf8;