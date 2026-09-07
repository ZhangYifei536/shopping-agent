## Day1:完成数据库搭建、环境搭建
在本地MySQL搭建一个商品数据库表：
create database shopping_agent
default character set utf8mb4
collate utf8mb4_unicode_ci

在dataset shopping_agent中：
CREATE TABLE product (
                         id BIGINT PRIMARY KEY AUTO_INCREMENT,

                         name VARCHAR(100) NOT NULL COMMENT '商品名称',
                         category VARCHAR(50) NOT NULL COMMENT '商品类别',
                         specification VARCHAR(50) COMMENT '商品规格',

                         price DECIMAL(10,2) NOT NULL COMMENT '单价/元',

                         calories DECIMAL(10,2) COMMENT '能量 kcal/100g',
                         protein DECIMAL(10,2) COMMENT '蛋白质 g/100g',
                         fat DECIMAL(10,2) COMMENT '脂肪 g/100g',
                         carbohydrate DECIMAL(10,2) COMMENT '碳水化合物 g/100g'
);

在backend/scripts/import_data.py中实现把csv数据导入product表
