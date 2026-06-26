-- ============================================================
-- 个性化网络学习空间 · MySQL 建库脚本
-- 运行方式：mysql -u root -p < mysql_init.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS learning_space
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE learning_space;

-- 创建一个专用账号（可选，也可直接用 root）
CREATE USER IF NOT EXISTS 'learn_user'@'localhost' IDENTIFIED BY 'Learn@123456';
GRANT ALL PRIVILEGES ON learning_space.* TO 'learn_user'@'localhost';
FLUSH PRIVILEGES;

SELECT '✅ 数据库 learning_space 创建完成' AS result;
