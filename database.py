import pymysql

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Cnsa0424.",
    "database": "restaurant_db",
    "charset": "utf8mb4"
}

def get_conn():
    return pymysql.connect(**DB_CONFIG)

#初始化数据库
def init_db():
    conn = get_conn()
    c=conn.cursor()

    #创建用户表
    c.execute('''CREATE TABLE IF NOT EXISTS user
    (ID INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(50),
    taste VARCHAR(20),
    consume VARCHAR(20))''')

    #创建餐厅表
    c.execute('''CREATE TABLE IF NOT EXISTS restaurant
    (rname VARCHAR(50) UNIQUE,
    food_type VARCHAR(50),
    avg_price INT,
    score FLOAT,
    address VARCHAR(100))''')

    #创建评价表
    c.execute('''CREATE TABLE IF NOT EXISTS comment
    (cID INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50),
    rname VARCHAR(50),
    score FLOAT,
    content TEXT)''')

    conn.commit()
    conn.close()
