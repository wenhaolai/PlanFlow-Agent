-- 设置字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS planflow_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE planflow_db;

CREATE TABLE tasks (
    id INT NOT NULL AUTO_INCREMENT COMMENT '任务ID',
    user_id INT NOT NULL COMMENT '用户ID',
    title VARCHAR(255) NOT NULL COMMENT '对话标题',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    PRIMARY KEY (id),
    INDEX idx_user_id (user_id),
    CONSTRAINT fk_task_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='任务(对话)表';

CREATE TABLE chat (
    id INT NOT NULL AUTO_INCREMENT COMMENT '聊天ID',
    task_id INT NOT NULL COMMENT '所属任务ID',
    role VARCHAR(50) NOT NULL COMMENT '角色',
    content TEXT NOT NULL COMMENT '对话内容',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '时间戳',

    PRIMARY KEY (id),
    INDEX idx_task_id (task_id),
    CONSTRAINT fk_chat_task FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='聊天记录表';