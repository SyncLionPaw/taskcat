-- 修改现有字段的属性
ALTER TABLE tasks
    MODIFY description MEDIUMTEXT,
    MODIFY created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    MODIFY updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    MODIFY progress FLOAT DEFAULT NULL,
    MODIFY difficulty INT DEFAULT 1,
    MODIFY points INT DEFAULT 0;

-- 添加新字段
ALTER TABLE tasks
    ADD COLUMN publish_type INT NOT NULL DEFAULT 1,
    ADD COLUMN deadline DATETIME,
    ADD COLUMN material_id INT NOT NULL;

-- 添加外键约束
ALTER TABLE tasks
    ADD CONSTRAINT fk_tasks_material_id FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_tasks_creator_id FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_tasks_assignee_id FOREIGN KEY (assignee_id) REFERENCES users(id) ON DELETE SET NULL;

-- 添加索引
CREATE INDEX ix_tasks_creator_id ON tasks(creator_id);
CREATE INDEX ix_tasks_assignee_id ON tasks(assignee_id);
CREATE INDEX ix_tasks_material_id ON tasks(material_id);
CREATE INDEX ix_tasks_created_at ON tasks(created_at);
