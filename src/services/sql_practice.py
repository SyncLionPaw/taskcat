import os
import uuid
import asyncio
import re
from datetime import datetime, timedelta
import docker
import mysql.connector
import json

class SQLPracticeService:
    """SQL练习服务，管理Docker容器中的MySQL数据库实例"""
    
    def __init__(self):
        """初始化Docker客户端和基本配置"""
        self.docker_client = docker.from_env()
        self.mysql_image = "mysql:8.0"
        self.mysql_root_password = "practice_password"
        self.mysql_database = "practice_db"
        self.mysql_user = "practice_user"
        self.mysql_password = "practice_password"
        self.container_expiry = timedelta(hours=1)  # 容器有效期1小时
        
        # 初始化脚本和验证脚本
        self.scripts_dir = os.path.join(os.path.dirname(__file__), "../scripts/sql_practice")
        os.makedirs(self.scripts_dir, exist_ok=True)
        
        # 确保初始化脚本存在
        self._ensure_init_scripts()
        
    async def _ensure_init_scripts(self):
        """确保初始化脚本存在，如果不存在则创建"""
        # 简单难度初始化脚本
        easy_script_path = os.path.join(self.scripts_dir, "init_easy.sql")
        if not os.path.exists(easy_script_path):
            with open(easy_script_path, "w") as f:
                f.write("""
-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    age INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建订单表
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 插入示例数据
INSERT INTO users (name, email, age) VALUES
('张三', 'zhang@example.com', 24),
('李四', 'li@example.com', 28),
('王五', 'wang@example.com', 32);

INSERT INTO orders (user_id, amount) VALUES
(1, 200.50),
(1, 100.00),
(2, 150.75),
(3, 100.00),
(3, 320.00);
                """)
        
        # 中等难度初始化脚本
        medium_script_path = os.path.join(self.scripts_dir, "init_medium.sql")
        if not os.path.exists(medium_script_path):
            with open(medium_script_path, "w") as f:
                f.write("""
-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    age INT,
    city VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建订单表
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 创建产品表
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建订单项表
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- 插入示例数据
INSERT INTO users (name, email, age, city) VALUES
('张三', 'zhang@example.com', 24, '北京'),
('李四', 'li@example.com', 28, '上海'),
('王五', 'wang@example.com', 32, '广州'),
('赵六', 'zhao@example.com', 45, '北京'),
('钱七', 'qian@example.com', 36, '深圳');

INSERT INTO products (name, price, category) VALUES
('笔记本电脑', 6999.00, '电子产品'),
('智能手机', 3999.00, '电子产品'),
('书桌', 1299.00, '家具'),
('办公椅', 599.00, '家具'),
('耳机', 299.00, '配件');

INSERT INTO orders (user_id, amount, status) VALUES
(1, 7598.00, 'completed'),
(1, 3999.00, 'pending'),
(2, 1299.00, 'completed'),
(3, 6999.00, 'completed'),
(4, 898.00, 'completed'),
(5, 4598.00, 'pending');

INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 6999.00),
(1, 5, 2, 299.00),
(2, 2, 1, 3999.00),
(3, 3, 1, 1299.00),
(4, 1, 1, 6999.00),
(5, 4, 1, 599.00),
(5, 5, 1, 299.00),
(6, 2, 1, 3999.00),
(6, 5, 2, 299.00);
                """)
                
        # 困难难度初始化脚本
        hard_script_path = os.path.join(self.scripts_dir, "init_hard.sql")
        if not os.path.exists(hard_script_path):
            with open(hard_script_path, "w") as f:
                f.write("""
-- 创建复杂的多表关系模型
-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    age INT,
    city VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 部门表
CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    budget DECIMAL(12, 2) NOT NULL,
    city VARCHAR(100)
);

-- 员工表
CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    department_id INT NOT NULL,
    position VARCHAR(100) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL,
    hire_date DATE NOT NULL,
    manager_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (manager_id) REFERENCES employees(id)
);

-- 项目表
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    budget DECIMAL(12, 2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    department_id INT,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- 项目分配表
CREATE TABLE IF NOT EXISTS project_assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    employee_id INT NOT NULL,
    role VARCHAR(50) NOT NULL,
    assigned_date DATE NOT NULL,
    hours_allocated INT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

-- 时间记录表
CREATE TABLE IF NOT EXISTS time_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    project_id INT NOT NULL,
    work_date DATE NOT NULL,
    hours_worked DECIMAL(4, 2) NOT NULL,
    description TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- 插入示例数据
INSERT INTO users (name, email, age, city) VALUES
('张三', 'zhang@example.com', 30, '北京'),
('李四', 'li@example.com', 32, '上海'),
('王五', 'wang@example.com', 28, '广州'),
('赵六', 'zhao@example.com', 35, '深圳'),
('钱七', 'qian@example.com', 40, '北京'),
('孙八', 'sun@example.com', 26, '上海'),
('周九', 'zhou@example.com', 38, '广州');

INSERT INTO departments (name, budget, city) VALUES
('研发部', 2000000.00, '北京'),
('市场部', 1500000.00, '上海'),
('财务部', 1000000.00, '广州'),
('人力资源部', 800000.00, '深圳'),
('行政部', 500000.00, '北京');

-- 插入员工数据（先插入一些没有manager的）
INSERT INTO employees (user_id, department_id, position, salary, hire_date) VALUES
(1, 1, '技术总监', 30000.00, '2018-01-10'),
(5, 2, '市场总监', 28000.00, '2019-03-15'),
(4, 3, '财务总监', 25000.00, '2017-07-22');

-- 更新插入manager_id
INSERT INTO employees (user_id, department_id, position, salary, hire_date, manager_id) VALUES
(2, 1, '高级开发', 18000.00, '2019-05-20', 1),
(3, 1, '开发工程师', 15000.00, '2020-01-10', 2),
(6, 2, '市场专员', 12000.00, '2020-03-15', 5),
(7, 3, '会计', 10000.00, '2021-02-18', 4);

INSERT INTO projects (name, budget, start_date, end_date, department_id, status) VALUES
('移动应用开发', 500000.00, '2022-01-01', '2022-06-30', 1, 'completed'),
('网站改版', 300000.00, '2022-03-15', '2022-08-30', 1, 'in_progress'),
('市场推广活动', 200000.00, '2022-02-01', '2022-05-30', 2, 'completed'),
('财务系统升级', 400000.00, '2022-04-01', NULL, 3, 'in_progress'),
('员工培训计划', 100000.00, '2022-05-01', NULL, 4, 'planning');

INSERT INTO project_assignments (project_id, employee_id, role, assigned_date, hours_allocated) VALUES
(1, 1, '项目经理', '2022-01-01', 120),
(1, 2, '技术负责人', '2022-01-01', 160),
(1, 3, '开发人员', '2022-01-15', 180),
(2, 2, '技术负责人', '2022-03-15', 140),
(2, 3, '开发人员', '2022-03-15', 180),
(3, 5, '项目经理', '2022-02-01', 100),
(3, 6, '市场专员', '2022-02-01', 150),
(4, 4, '项目经理', '2022-04-01', 80),
(4, 7, '财务分析', '2022-04-01', 120);

INSERT INTO time_records (employee_id, project_id, work_date, hours_worked, description) VALUES
(1, 1, '2022-01-10', 8.00, '项目启动会议和规划'),
(2, 1, '2022-01-10', 8.00, '技术方案设计'),
(3, 1, '2022-01-20', 7.50, '功能开发'),
(2, 2, '2022-03-20', 8.00, '架构设计'),
(3, 2, '2022-03-22', 8.00, '前端开发'),
(5, 3, '2022-02-10', 6.00, '市场策略制定'),
(6, 3, '2022-02-15', 8.00, '执行市场计划'),
(4, 4, '2022-04-05', 5.00, '需求分析'),
(7, 4, '2022-04-10', 8.00, '系统测试');
                """)
        
    def _get_init_script_path(self, difficulty):
        """获取对应难度的初始化脚本路径"""
        script_name = f"init_{difficulty}.sql"
        return os.path.join(self.scripts_dir, script_name)
        
    async def get_user_database(self, user_id):
        """获取用户当前的数据库实例"""
        try:
            containers = await asyncio.to_thread(
                self.docker_client.containers.list,
                all=True,
                filters={"label": [f"user_id={user_id}"]}
            )
            
            if not containers:
                return None
                
            # 选择最新创建的容器
            containers.sort(key=lambda c: c.attrs['Created'], reverse=True)
            container = containers[0]
            
            return await self._format_container_info(container)
        except Exception as e:
            print(f"Error getting user database: {e}")
            return None
            
    async def create_database(self, user_id, username="default_user", difficulty="easy"):
        """为用户创建新的数据库实例"""
        try:
            # 清理用户名，确保可以作为数据库名称
            sanitized_username = self._sanitize_db_name(username)
            db_name = f"db_{sanitized_username}"
            
            # 创建唯一的容器名称
            container_name = f"sql-{sanitized_username}-{uuid.uuid4().hex[:8]}"
            
            # 设置容器过期时间
            expires_at = datetime.now() + self.container_expiry
            
            # 创建容器
            container = await asyncio.to_thread(
                self.docker_client.containers.run,
                self.mysql_image,
                name=container_name,
                detach=True,
                environment={
                    "MYSQL_ROOT_PASSWORD": self.mysql_root_password,
                    "MYSQL_DATABASE": db_name,  # 使用用户名创建数据库
                    "MYSQL_USER": self.mysql_user,
                    "MYSQL_PASSWORD": self.mysql_password
                },
                ports={'3306/tcp': None},  # 自动分配端口
                labels={
                    "user_id": str(user_id),
                    "username": username,
                    "db_name": db_name,
                    "expires_at": expires_at.isoformat(),
                    "difficulty": difficulty
                }
            )
            
            # 等待MySQL启动
            await self._wait_for_mysql(container, db_name)
            
            # 初始化数据库
            await self._initialize_database(container, difficulty, db_name)
            
            return await self._format_container_info(container)
        except Exception as e:
            print(f"Error creating database: {e}")
            raise
    
    # 辅助方法：清理用户名，使其可作为数据库名称
    def _sanitize_db_name(self, username):
        # 移除非法字符，只保留字母、数字和下划线
        sanitized = re.sub(r'[^\w]', '_', username)
        # 确保不是纯数字且不为空
        if sanitized.isdigit() or not sanitized:
            sanitized = f"user_{sanitized}"
        # 数据库名称长度限制
        return sanitized[:32]
        
    async def _wait_for_mysql(self, container, db_name, max_retries=20):
        """等待MySQL服务启动"""
        container_info = await asyncio.to_thread(container.reload)
        port = container_info.attrs['NetworkSettings']['Ports']['3306/tcp'][0]['HostPort']
        
        retries = 0
        while retries < max_retries:
            try:
                # 尝试连接MySQL
                conn = mysql.connector.connect(
                    host='localhost',
                    port=port,
                    user='root',
                    password=self.mysql_root_password,
                    database=db_name,  # 使用创建的数据库名
                    connection_timeout=2
                )
                conn.close()
                return True  # 连接成功
            except Exception:
                # 连接失败，等待后重试
                await asyncio.sleep(1)
                retries += 1
        
        # 超出重试次数
        raise Exception("MySQL服务启动超时")
            
    async def _initialize_database(self, container, difficulty, db_name=None):
        """使用初始化脚本初始化数据库"""
        try:
            container_info = await asyncio.to_thread(container.reload)
            port = container_info.attrs['NetworkSettings']['Ports']['3306/tcp'][0]['HostPort']
            
            # 如果没有提供数据库名，使用默认值
            database = db_name or self.mysql_database
            
            # 读取初始化脚本
            script_path = self._get_init_script_path(difficulty)
            with open(script_path, 'r') as f:
                init_script = f.read()
            
            # 连接MySQL并执行初始化脚本
            conn = mysql.connector.connect(
                host='localhost',
                port=port,
                user='root',
                password=self.mysql_root_password,
                database=database
            )
            cursor = conn.cursor()
            
            # 支持多语句执行
            for statement in init_script.split(';'):
                if statement.strip():
                    cursor.execute(statement)
                    
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise
            
    async def get_database_info(self, database_id):
        """获取数据库容器信息"""
        try:
            container = await asyncio.to_thread(
                self.docker_client.containers.get,
                database_id
            )
            return await self._format_container_info(container)
        except Exception as e:
            print(f"Error getting database info: {e}")
            return None
            
    async def reset_database(self, database_id, difficulty="easy"):
        """重置数据库到初始状态"""
        try:
            container = await asyncio.to_thread(
                self.docker_client.containers.get,
                database_id
            )
            
            # 确保容器正在运行
            if container.status != 'running':
                await asyncio.to_thread(container.start)
                await self._wait_for_mysql(container)
                
            # 重新初始化数据库
            await self._initialize_database(container, difficulty)
            
            return True
        except Exception as e:
            print(f"Error resetting database: {e}")
            raise
            
    async def execute_query(self, database_id, sql, question_id=None, difficulty=None):
        """执行SQL查询"""
        try:
            container = await asyncio.to_thread(
                self.docker_client.containers.get,
                database_id
            )
            
            # 确保容器正在运行
            if container.status != 'running':
                raise Exception("数据库实例未运行")
                
            # 获取端口
            port = container.attrs['NetworkSettings']['Ports']['3306/tcp'][0]['HostPort']
            
            # 获取数据库名称
            db_name = container.labels.get('db_name', self.mysql_database)
            
            # 连接数据库
            conn = mysql.connector.connect(
                host='localhost',
                port=port,
                user=self.mysql_user,
                password=self.mysql_password,
                database=db_name  # 使用容器标签中的数据库名
            )
            
            cursor = conn.cursor(dictionary=True)
            
            # 执行查询，并测量执行时间
            start_time = datetime.now()
            cursor.execute(sql)
            end_time = datetime.now()
            
            # 如果是SELECT查询，获取结果
            results = None
            affected_rows = 0
            
            if cursor.description:  # SELECT查询
                results = cursor.fetchall()
            else:  # INSERT, UPDATE, DELETE等
                affected_rows = cursor.rowcount
                conn.commit()
            
            execution_time = (end_time - start_time).total_seconds() * 1000  # 毫秒
            
            # 检查查询是否正确（如果提供了问题ID和难度）
            is_correct = False
            if question_id and difficulty:
                # 这里可以实现与预期查询结果的比较
                # 简单的实现：根据行数和列数检查
                expected_result = await self._get_expected_result(difficulty, question_id)
                if expected_result and results:
                    # 简单检查：行数一致且关键列存在
                    is_correct = (len(results) == len(expected_result))
                    if is_correct and len(results) > 0:
                        for key in expected_result[0].keys():
                            if key not in results[0]:
                                is_correct = False
                                break
            
            cursor.close()
            conn.close()
            
            # 返回结果
            return {
                "results": results or [],
                "executionTime": int(execution_time),
                "affectedRows": affected_rows,
                "isCorrect": is_correct
            }
        except Exception as e:
            print(f"Error executing query: {e}")
            raise
            
    async def _get_expected_result(self, difficulty, question_id):
        """获取预期的查询结果"""
        # 这里可以从文件或者直接从代码中获取预期结果
        # 简单实现：根据难度和问题ID返回预定义的结果
        expected_results = {
            "easy": {
                1: [
                    {"id": 1, "name": "张三", "email": "zhang@example.com"},
                    {"id": 2, "name": "李四", "email": "li@example.com"},
                    {"id": 3, "name": "王五", "email": "wang@example.com"}
                ],
                2: [
                    {"id": 2, "name": "李四", "email": "li@example.com", "age": 28, "created_at": "2023-01-15 10:30:00"},
                    {"id": 3, "name": "王五", "email": "wang@example.com", "age": 32, "created_at": "2023-02-20 14:45:00"}
                ]
            },
            "medium": {
                1: [
                    {"id": 1, "name": "张三", "total_amount": 300.50},
                    {"id": 2, "name": "李四", "total_amount": 150.75},
                    {"id": 3, "name": "王五", "total_amount": 420.00}
                ]
            },
            "hard": {
                1: [
                    {"id": 1, "name": "张三", "order_id": 1, "amount": 200.50},
                    {"id": 3, "name": "王五", "order_id": 5, "amount": 320.00}
                ]
            }
        }
        
        return expected_results.get(difficulty, {}).get(int(question_id), [])
            
    async def delete_database(self, database_id):
        """删除数据库实例"""
        try:
            container = await asyncio.to_thread(
                self.docker_client.containers.get,
                database_id
            )
            
            # 停止并删除容器
            await asyncio.to_thread(container.stop)
            await asyncio.to_thread(container.remove)
            
            return True
        except Exception as e:
            print(f"Error deleting database: {e}")
            raise
            
    async def cleanup_user_databases(self, user_id):
        """清理用户的所有数据库实例"""
        try:
            containers = await asyncio.to_thread(
                self.docker_client.containers.list,
                all=True,
                filters={"label": [f"user_id={user_id}"]}
            )
            
            for container in containers:
                await asyncio.to_thread(container.stop, timeout=5)
                await asyncio.to_thread(container.remove)
                
            return True
        except Exception as e:
            print(f"Error cleaning up user databases: {e}")
            raise
            
    async def _format_container_info(self, container):
        """格式化容器信息为API响应格式"""
        try:
            # 刷新容器信息
            container_info = await asyncio.to_thread(container.reload)
            
            # 从标签中获取元数据
            user_id = container_info.labels.get('user_id')
            username = container_info.labels.get('username')
            db_name = container_info.labels.get('db_name')
            expires_at = container_info.labels.get('expires_at')
            difficulty = container_info.labels.get('difficulty', 'easy')
            
            # 获取端口映射
            port = None
            if container_info.attrs['State']['Status'] == 'running':
                ports = container_info.attrs['NetworkSettings']['Ports']
                if '3306/tcp' in ports and ports['3306/tcp']:
                    port = ports['3306/tcp'][0]['HostPort']
                    
            return {
                "id": container_info.id,
                "name": container_info.name,
                "user_id": user_id,
                "username": username,
                "dbName": db_name,
                "status": container_info.status,
                "created": container_info.attrs['Created'],
                "expiresAt": expires_at,
                "difficulty": difficulty,
                "port": port
            }
        except Exception as e:
            print(f"Error formatting container info: {e}")
            raise
