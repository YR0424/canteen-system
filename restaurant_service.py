import pymysql
from database import get_conn
#添加餐厅
def add_restaurant(rname, food_type, avg_price, score, address):
    conn = get_conn()
    c = conn.cursor()

    try:
        c.execute(
            """
            INSERT INTO restaurant
            (rname,food_type,avg_price,score,address)
            VALUES(%s,%s,%s,%s,%s)
            """,
            (rname, food_type, avg_price, score, address)
        )

        conn.commit()
        return True

    except pymysql.IntegrityError:
        return False

    finally:
        conn.close()
#查看所有餐厅
def get_all_restaurants():
    conn = get_conn()
    c = conn.cursor()

    c.execute(
        """
        SELECT * FROM restaurant
        """
    )

    data = c.fetchall()
    conn.close()

    return data
#餐厅推荐
def show_recommend(username):
    conn = get_conn()
    c = conn.cursor()

    c.execute(
        """
        SELECT taste,consume FROM user WHERE username=%s
        """,
        (username,)
    )

    result = c.fetchone()
    if not result:
        conn.close()
        return []

    user_taste, user_consume = result
    price_map={
        "低": (0, 50),
        "中": (50, 100),
        "高": (100, 999)
    }

    min_price, max_price = price_map.get(user_consume, (0, 999))

    c.execute(
        """
        SELECT * FROM restaurant WHERE food_type=%s AND avg_price BETWEEN %s AND %s ORDER BY score DESC
        """,
        (f"{user_taste}%", min_price, max_price)
    )

    data = c.fetchall()
    conn.close()

    return data
#添加餐厅评价
def show_add_comment(username, rname, score, content):
    conn = get_conn()
    c = conn.cursor()

    c.execute(
        """
        SELECT * FROM restaurant WHERE rname=%s
        """,
        (rname,)
    )

    if not c.fetchone():
        conn.close()
        return False

   
    c.execute(
        """
        INSERT INTO comment
        (username,rname,score,content)
        VALUES(%s,%s,%s,%s)
        """,
        (username, rname, score, content)
    )

    conn.commit()
    conn.close()

    return True
