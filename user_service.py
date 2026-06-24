import pymysql
from database import get_conn

def register_user(username, password, taste, consume):
    conn = get_conn()
    c = conn.cursor()

    try:
        c.execute(
            """
            INSERT INTO user(username,password,taste,consume)
            VALUES(%s,%s,%s,%s)
            """,
            (username, password, taste, consume)
        )

        conn.commit()
        return True

    except pymysql.IntegrityError:
        return False

    finally:
        conn.close()

def login_user(username,password):
    conn = get_conn()
    c = conn.cursor()

    c.execute(
        """
        SELECT * FROM user WHERE username=%s AND password=%s
        """,
        (username, password)
    )

    user = c.fetchone()
    conn.close()

    return user