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
#搜索餐厅
def search_restaurant(keyword):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """
        SELECT * FROM restaurant 
        WHERE 
        rname LIKE %s
        OR food_type LIKE %s
        OR address LIKE %s
        """,
        (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
    )
    result = c.fetchall()
    conn.close()
    return result

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
    #1.查询用户偏好
    c.execute(
        """
        SELECT taste,consume FROM user WHERE username=%s
        """,
        (username,)
    )
    user_info =c.fetchone()
    if not user_info:
        conn.close()
        return []
    taste, consume = user_info
    #2.查询所有餐厅
    c.execute(
        """
        SELECT * FROM restaurant 
        """
    )   
    restaurants = c.fetchall()
    #3.设置消费标准
    price_map = {
        "低": 50,
        "中": 100,
        "高": 999
    }
    max_price=price_map.get(consume, 999)
    recommend_list=[]
    #4，计算餐厅推荐分
    for r in restaurants:
        rname, food_type, avg_price, score, address = r
        #查询用户评价平均分
        c.execute(
            """
            SELECT AVG(score) FROM comment WHERE rname=%s
            """,
            (rname,)
        )
        comment_score = c.fetchone()[0]
        if comment_score is None:
            comment_score = 0
        #口味匹配分
        taste_score = 0
        if taste in food_type :
            taste_score = 40
        #价格匹配分
        price_score = 0
        if avg_price <= max_price:
            price_score = 20
        #评分分
        score_score = score * 8
        comment_score_value = comment_score * 8
        #总推荐分
        total_score = (taste_score/40)*40 + (price_score/20)*20 + (score_score/40)*20 + (comment_score_value/40)*20
        #根据推荐分判断等级
        if total_score >= 85:
            level = "强烈推荐"
        elif total_score >= 70:
            level = "推荐" 
        else:
            level = "一般"
        #生成推荐理由
        reasons = []
        if taste_score == 40:
            reasons.append("口味符合偏好")
        if price_score == 20:
            reasons.append("价格符合消费水平")
        if score >= 4.5:
            reasons.append("餐厅评分较高")
        if comment_score >= 4.5:
            reasons.append("评价不错")
        reason_text = "、".join(reasons) 
        recommend_list.append((rname, food_type, avg_price, score, address, round(total_score, 2), level, reason_text))
    #5.按推荐分排序
    recommend_list.sort(key=lambda x: x[5], reverse=True)
    print("排序后结果：")
    for r in recommend_list:
        print(r[0],r[5],r[6])
    conn.close()
    return recommend_list

#添加餐厅评价
def show_add_comment(username, rname, score, content):
    conn = get_conn()
    c = conn.cursor()

    c.execute(
        """
        SELECT * FROM restaurant WHERE TRIM(rname)=TRIM(%s)
        """,
        (rname,)
    )

    restaurant = c.fetchone()

    print("查询餐厅结果:", restaurant)

    if not restaurant:
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
    print("插入完成")
    conn.commit()
    print("提交完成")
    conn.close()
    return True
#查看餐厅评价
def show_comments(rname):
    conn = get_conn()
    c = conn.cursor()

    c.execute(
        """
        SELECT username, score, content 
        FROM comment 
        WHERE rname=%s
        """,
        (rname,)
    )

    data = c.fetchall()
    conn.close()
    return data
#热门餐厅排行榜
def get_hot_restaurants():
    conn = get_conn()
    c = conn.cursor()
    c.execute(
    """
    SELECT
        restaurant.rname,
        restaurant.food_type,
        restaurant.avg_price,
        IFNULL(ROUND(AVG(comment.score),2),0) AS avg_score,
        COUNT(comment.cID) AS comment_count
    FROM restaurant
    LEFT JOIN comment
    ON restaurant.rname = comment.rname
    GROUP BY
        restaurant.rname,
        restaurant.food_type,
        restaurant.avg_price
    ORDER BY avg_score DESC, comment_count DESC
    """
)
    data = c.fetchall()
    conn.close()
    return data
#收藏餐厅
# 收藏餐厅
def add_favorite(username, rname):
    conn = get_conn()
    c = conn.cursor()
    try:
        # 判断是否已经收藏
        c.execute(
            """
            SELECT * FROM favorite
            WHERE username=%s AND rname=%s
            """,
            (username, rname)
        )

        if c.fetchone():
            return False
        # 添加收藏
        c.execute(
            """
            INSERT INTO favorite
            (username,rname)
            VALUES(%s,%s)
            """,
            (username,rname)
        )

        conn.commit()
        return True

    finally:
        conn.close()

# 查看我的收藏
def get_favorite(username):

    conn = get_conn()
    c = conn.cursor()

    c.execute(
        """
        SELECT 
            restaurant.rname,
            restaurant.food_type,
            restaurant.avg_price,
            restaurant.score,
            restaurant.address
        FROM favorite
        JOIN restaurant
        ON favorite.rname=restaurant.rname
        WHERE favorite.username=%s
        """,
        (username,)
    )

    data=c.fetchall()
    conn.close()

    return data
