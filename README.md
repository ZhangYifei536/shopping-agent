## Day1:完成数据库搭建、环境搭建
在本地MySQL搭建一个商品数据库表：
    create database shopping_agent
    default character set utf8mb4
    collate utf8mb4_unicode_ci

在dataset shopping_agent中：
商品表，包含id，名称，类别，规格，价格，营养信息id

    CREATE TABLE product (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '商品名称',
    category VARCHAR(50) NOT NULL COMMENT '商品类别',
    specification VARCHAR(50) COMMENT '商品规格',
    price DECIMAL(10,2) NOT NULL COMMENT '商品价格',

    nutrition_id BIGINT,

    CONSTRAINT fk_product_nutrition
        FOREIGN KEY (nutrition_id)
        REFERENCES nutrition(id)
    );

营养信息表，包含id，总能量，总蛋白质，总脂肪，总碳水化合物

    CREATE TABLE nutrition (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    total_calories DECIMAL(10,2) COMMENT '整件商品总能量 kcal',
    total_protein DECIMAL(10,2) COMMENT '整件商品总蛋白质 g',
    total_fat DECIMAL(10,2) COMMENT '整件商品总脂肪 g',
    total_carbohydrate DECIMAL(10,2) COMMENT '整件商品总碳水 g'
    );

在backend/scripts/import_data.py中实现把csv数据导入product表

backend/app/database/db.py负责统一创建数据库连接
backend/app/tools/product_tools.py负责按照需求，执行SQL代码获取商品信息
backend/app/tools/recommend_tools.py负责根据预算和营养约束生成购物组合