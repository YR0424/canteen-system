# 智能餐厅推荐系统

## 项目简介

本项目基于 Python + Tkinter + MySQL 开发，实现了一个简单的智能餐厅推荐系统。

用户可以进行注册登录、查看餐厅信息、添加餐厅、发表评价，并根据个人口味偏好和消费水平获得餐厅推荐。

---

## 技术栈

- Python 3
- Tkinter（GUI界面开发）
- MySQL（数据库）
- PyMySQL（数据库连接）
- Git & GitHub（版本管理）

---

## 功能介绍

### 用户模块

- 用户注册
- 用户登录

### 餐厅模块

- 添加餐厅
- 查看全部餐厅

### 推荐模块

根据用户：

- 口味偏好
- 消费水平

进行智能推荐。

### 评论模块

- 发表餐厅评价

---

## 数据库设计

### user 用户表

| 字段 | 类型 | 说明 |
|--------|--------|--------|
| ID | INT | 用户ID |
| username | VARCHAR(50) | 用户名 |
| password | VARCHAR(50) | 密码 |
| taste | VARCHAR(20) | 口味偏好 |
| consume | VARCHAR(20) | 消费水平 |

---

### restaurant 餐厅表

| 字段 | 类型 | 说明 |
|--------|--------|--------|
| rname | VARCHAR(50) | 餐厅名称 |
| food_type | VARCHAR(50) | 菜系类型 |
| avg_price | INT | 人均价格 |
| score | FLOAT | 评分 |
| address | VARCHAR(100) | 地址 |

---

### comment 评论表

| 字段 | 类型 | 说明 |
|--------|--------|--------|
| cID | INT | 评论ID |
| username | VARCHAR(50) | 用户名 |
| rname | VARCHAR(50) | 餐厅名称 |
| score | FLOAT | 评分 |
| content | TEXT | 评论内容 |

---

## 项目结构

```text
canteen/

├── main.py                # GUI界面
├── database.py            # 数据库连接
├── user_service.py        # 用户业务逻辑
├── restaurant_service.py  # 餐厅业务逻辑
├── README.md
└── .gitignore
```

---

## 运行方法

### 1. 创建数据库

```sql
CREATE DATABASE restaurant_db;
```

### 2. 修改数据库配置

在 database.py 中配置：

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "你的数据库密码",
    "database": "restaurant_db",
    "charset": "utf8mb4"
}
```

### 3. 安装依赖

```bash
pip install pymysql
```

### 4. 运行项目

```bash
python main.py
```

---

## 项目特点

- 图形化界面操作
- MySQL数据库存储
- 模块化开发设计
- 用户偏好推荐
- Git版本管理

---

## 后续优化方向

- 密码加密存储
- 推荐算法优化
- 管理员功能
- 搜索餐厅功能
- 评论查看功能
- 数据可视化分析

