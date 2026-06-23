import pymysql
import tkinter as tk
from tkinter import messagebox,ttk

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_PASSWORD",
    "database": "restaurant_db",
    "charset": "utf8mb4"
}

#初始化数据库
def init_db():
    conn=pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        charset=DB_CONFIG["charset"]
    )
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

init_db()

class RestaurantGUI:
    def __init__(self,root):
        self.root=root
        self.root.title("智能餐厅推荐系统")
        self.root.geometry("720x520")
        self.root.resizable(False,False)
        self.current_user=None
        self.show_main_menu()

    def clear_win(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    #获取MySQL连接
    def get_conn(self):
        return pymysql.connect(**DB_CONFIG)

    #1.主菜单界面
    def show_main_menu(self):
        self.clear_win()
        tk.Label(self.root,text="智能餐厅推荐系统",font=("黑体",22)).pack(pady=35)

        btn_cfg={"width":22,"height":2,"font":("宋体",12)}
        tk.Button(self.root,text="用户注册",**btn_cfg,command=self.show_register).pack(pady=10)
        tk.Button(self.root, text="用户登录", **btn_cfg, command=self.show_login).pack(pady=10)
        tk.Button(self.root, text="添加餐厅", **btn_cfg, command=self.show_add_rest).pack(pady=10)
        tk.Button(self.root, text="查看所有餐厅", **btn_cfg, command=self.show_all_rest).pack(pady=10)
        tk.Button(self.root, text="退出系统", **btn_cfg, command=self.root.quit).pack(pady=10)

    #2.注册界面
    def show_register(self):
        self.clear_win()
        tk.Label(self.root, text="用户注册", font=("黑体", 18)).pack(pady=20)

        frame=tk.Frame(self.root)
        frame.pack()
        #用户名输入
        tk.Label(frame,text="用户名：",font=("宋体",12)).grid(row=0,column=0,padx=10,pady=8,sticky="w")
        ent_user=tk.Entry(frame,width=32,font=("宋体",12))
        ent_user.grid(row=0,column=1)
        #密码输入
        tk.Label(frame, text="密 码：", font=("宋体", 12)).grid(row=1, column=0, padx=10, pady=8, sticky="w")
        ent_pwd= tk.Entry(frame, width=32, font=("宋体", 12),show="*")
        ent_pwd.grid(row=1, column=1)
        #口味下拉框
        tk.Label(frame, text="口味偏好：", font=("宋体", 12)).grid(row=2, column=0, padx=10, pady=8, sticky="w")
        cb_taste= ttk.Combobox(frame, width=30, font=("宋体", 12))
        cb_taste["values"]=("麻辣","清淡","酸甜","鲜香")
        cb_taste.grid(row=2, column=1)
        #消费水平下拉框
        tk.Label(frame, text="消费水平：", font=("宋体", 12)).grid(row=3, column=0, padx=10, pady=8, sticky="w")
        cb_consume = ttk.Combobox(frame, width=30, font=("宋体", 12))
        cb_consume["values"] = ("低", "中", "高")
        cb_consume.grid(row=3, column=1)

        #注册逻辑
        def do_register():
            username=ent_user.get().strip()
            pwd=ent_pwd.get().strip()
            taste=cb_taste.get().strip()
            consume=cb_consume.get().strip()

            if not all([username,pwd,taste,consume]):
                messagebox.showwarning("提示","所有选项不能为空！")
                return

            conn=self.get_conn()
            c=conn.cursor()
            try:
                c.execute("INSERT INTO user(username,password,taste,consume) VALUES (%s,%s,%s,%s)",(username,pwd,taste,consume))
                conn.commit()
                messagebox.showinfo("成功","注册成功！")
                self.show_main_menu()
            except pymysql.IntegrityError:
                messagebox.showerror("错误", "用户名已存在，注册失败！")
            finally:
                conn.close()

        tk.Button(self.root,text="立即注册",font=("宋体",12),command=do_register).pack(pady=20)
        tk.Button(self.root, text="返回首页", font=("宋体", 12), command=self.show_main_menu).pack()

    #3.登录界面
    def show_login(self):
        self.clear_win()
        tk.Label(self.root, text="用户登录", font=("黑体", 18)).pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack()
        # 用户名输入
        tk.Label(frame, text="用户名：", font=("宋体", 12)).grid(row=0, column=0, padx=10, pady=10)
        ent_user = tk.Entry(frame, width=32, font=("宋体", 12))
        ent_user.grid(row=0, column=1)
        # 密码输入
        tk.Label(frame, text="密 码：", font=("宋体", 12)).grid(row=1, column=0, padx=10, pady=10)
        ent_pwd = tk.Entry(frame, width=32, font=("宋体", 12), show="*")
        ent_pwd.grid(row=1, column=1)

        #登录逻辑
        def do_login():
            username=ent_user.get().strip()
            pwd=ent_pwd.get().strip()
            if not username or not pwd:
                messagebox.showwarning("提示","用户名和密码不能为空！")
                return

            conn=self.get_conn()
            c=conn.cursor()
            c.execute("SELECT * FROM user WHERE username=%s AND password=%s",(username,pwd))
            result = c.fetchone()
            conn.close()

            if result:
                self.current_user=username
                messagebox.showinfo("成功", "登录成功！")
                self.show_user_func()
            else:
                messagebox.showerror("错误", "账号或密码错误！")

        tk.Button(self.root, text="登 录", font=("宋体", 12), command=do_login).pack(pady=20)
        tk.Button(self.root, text="返回首页", font=("宋体", 12), command=self.show_main_menu).pack()

    #4.用户功能面板
    def show_user_func(self):
        self.clear_win()
        tk.Label(self.root,text=f"欢迎您：{self.current_user}",font=("黑体",16)).pack(pady=25)

        btn_cfg={"width":22,"height":2,"font":("宋体",12)}
        tk.Button(self.root,text="智能推荐餐厅",**btn_cfg,command=self.show_recommend).pack(pady=10)
        tk.Button(self.root, text="发表餐厅评价", **btn_cfg, command=self.show_add_commend).pack(pady=10)
        tk.Button(self.root, text="返回首页", **btn_cfg, command=self.show_main_menu).pack(pady=10)

    #5.智能推荐
    def show_recommend(self):
        self.clear_win()
        tk.Label(self.root,text="智能餐厅推荐",font=("黑体",18)).pack(pady=15)

        #表格组件
        cols=("餐厅名","菜系","人均价格","评分","地址")
        tree=ttk.Treeview(self.root,columns=cols,show="headings",height=10)
        for c in cols:
            tree.heading(c,text=c)
            tree.column(c,width=130)
        tree.pack(pady=10)

        conn=self.get_conn()
        cur=conn.cursor()
        #获取用户口味和消费水平
        cur.execute("SELECT taste,consume FROM user WHERE username=%s",(self.current_user,))
        user_taste,user_consume=cur.fetchone()
        #价格区间
        price_map={"低":(0,50),"中":(50,100),"高":(100,999)}
        min_price,max_price=price_map.get(user_consume,(0,999))

        cur.execute('''SELECT * FROM restaurant
                    WHERE food_type LIKE %s
                    AND avg_price BETWEEN %s AND %s
                    ORDER BY score DESC''',(f"%{user_taste}%",min_price,max_price))
        res_list=cur.fetchall()
        conn.close()

        if res_list:
            for r in res_list:
                tree.insert("","end",values=r)
        else:
            messagebox.showinfo("提示","暂无匹配的推荐餐厅！")

        tk.Button(self.root,text="返回",font=("宋体",12),command=self.show_user_func).pack(pady=10)

    #6.发表评论
    def show_add_commend(self):
        self.clear_win()
        tk.Label(self.root,text="发表餐厅评价",font=("黑体",18)).pack(pady=20)

        frame=tk.Frame(self.root)
        frame.pack()

        tk.Label(frame,text="餐厅名称：",font=("宋体",12)).grid(row=0,column=0,padx=10, pady=8)
        ent_rname=tk.Entry(frame,width=32,font=("宋体",12))
        ent_rname.grid(row=0,column=1)

        tk.Label(frame, text="你的评分：",font=("宋体", 12)).grid(row=1, column=0, padx=10, pady=8)
        ent_score = tk.Entry(frame, width=32, font=("宋体", 12))
        ent_score.grid(row=1, column=1)

        tk.Label(frame, text="评价内容：", font=("宋体", 12)).grid(row=2, column=0, padx=10, pady=8)
        ent_content = tk.Entry(frame, width=32, font=("宋体", 12))
        ent_content.grid(row=2, column=1)

        def submit_commend():
            rname=ent_rname.get().strip()
            content=ent_content.get().strip()
            if not rname or not content:
                messagebox.showwarning("提示","餐厅名和评价内容不能为空！")
                return
            try:
                u_score=float(ent_score.get().strip())
            except:
                messagebox.showwarning("提示","评分必须填入数字！")
                return

            conn=self.get_conn()
            c=conn.cursor()
            c.execute("SELECT * FROM restaurant WHERE rname=%s", (rname,))
            if not c.fetchone():
                messagebox.showerror("错误", "该餐厅不存在！")
                conn.close()
                return
            c.execute("INSERT INTO comment(username,rname,score,content) VALUES(%s,%s,%s,%s)",(self.current_user,rname,u_score,content))
            conn.commit()
            conn.close()
            messagebox.showinfo("成功","评论提交成功！")
            self.show_user_func()
        tk.Button(self.root,text="提交评论",font=("宋体",12),command=submit_commend).pack(pady=20)
        tk.Button(self.root,text="返回",font=("宋体",12),command=self.show_user_func).pack(pady=20)

    #7.添加餐厅
    def show_add_rest(self):
        self.clear_win()
        tk.Label(self.root,text="添加新餐厅",font=("黑体",18)).pack(pady=20)

        frame=tk.Frame(self.root)
        frame.pack()

        tk.Label(frame,text="餐厅名称：",font=("宋体",12)).grid(row=0,column=0,padx=10, pady=8)
        ent_rname=tk.Entry(frame,width=32,font=("宋体",12))
        ent_rname.grid(row=0,column=1)

        tk.Label(frame, text="菜系类型：", font=("宋体", 12)).grid(row=1, column=0, padx=10, pady=8)
        ent_type = tk.Entry(frame, width=32, font=("宋体", 12))
        ent_type.grid(row=1, column=1)

        tk.Label(frame, text="人均价格：", font=("宋体", 12)).grid(row=2, column=0, padx=10, pady=8)
        ent_price = tk.Entry(frame, width=32, font=("宋体", 12))
        ent_price.grid(row=2, column=1)

        tk.Label(frame, text="餐厅评分：", font=("宋体", 12)).grid(row=3, column=0, padx=10, pady=8)
        ent_score = tk.Entry(frame, width=32, font=("宋体", 12))
        ent_score.grid(row=3, column=1)

        tk.Label(frame, text="餐厅地址：", font=("宋体", 12)).grid(row=4, column=0, padx=10, pady=8)
        ent_addr = tk.Entry(frame, width=32, font=("宋体", 12))
        ent_addr.grid(row=4, column=1)

        def add_rest():
            rname=ent_rname.get().strip()
            ftype=ent_type.get().strip()
            addr=ent_addr.get().strip()
            if not all([rname,ftype,addr]):
                messagebox.showwarning("提示","信息不能为空！")
                return
            try:
                price=int(ent_price.get().strip())
                score=float(ent_score.get().strip())
            except:
                messagebox.showwarning("提示","价格、评分必须为数字")
                return

            conn=self.get_conn()
            c=conn.cursor()
            try:
                c.execute("INSERT INTO restaurant(rname,food_type,avg_price,score,address) VALUES (%s,%s,%s,%s,%s)", (rname,ftype,price,score,addr))
                conn.commit()
                conn.close()
                messagebox.showinfo("成功","餐厅添加成功！")
                self.show_main_menu()
            except pymysql.IntegrityError:
                messagebox.showerror("错误","餐厅已存在！")
            finally:
                conn.close()

        tk.Button(self.root,text="添加餐厅",font=("宋体",12),command=add_rest).pack(pady=20)
        tk.Button(self.root, text="返回首页", font=("宋体", 12), command=self.show_main_menu).pack()

    #8.查看全部餐厅
    def show_all_rest(self):
        self.clear_win()
        tk.Label(self.root,text="全部餐厅列表",font=("黑体",18)).pack(pady=15)

        cols=("餐厅名","菜系","人均价格","评分","地址")
        tree=ttk.Treeview(self.root,columns=cols,show="headings",height=10)
        for c in cols:
            tree.heading(c,text=c)
            tree.column(c,width=130)
        tree.pack(pady=10)

        conn=self.get_conn()
        c=conn.cursor()
        c.execute("SELECT * FROM restaurant")
        data=c.fetchall()
        conn.close()

        for item in data:
            tree.insert('','end',values=item)

        tk.Button(self.root,text="返回首页",font=("宋体",12),command=self.show_main_menu).pack(pady=10)


if __name__ == "__main__":
    root=tk.Tk()
    app=RestaurantGUI(root)
    root.mainloop()
    























