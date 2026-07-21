import pymysql
import tkinter as tk
from tkinter import messagebox,ttk
from user_service import register_user,login_user
from restaurant_service import (add_restaurant,get_all_restaurants,search_restaurant,show_recommend,show_add_comment,get_hot_restaurants,add_favorite,get_favorite )

from database import get_conn,init_db
init_db()

class RestaurantGUI:
    def __init__(self,root):
        self.root=root
        self.root.title("智能餐厅推荐系统")
        self.root.geometry("1300x600")
        self.root.resizable(False,False)
        self.current_user=None
        self.show_main_menu()

    def clear_win(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    #1.主菜单界面
    def show_main_menu(self):
        self.clear_win()
        tk.Label(self.root,text="智能餐厅推荐系统",font=("黑体",22)).pack(pady=35)

        btn_cfg={"width":22,"height":1,"font":("宋体",12)}
        tk.Button(self.root,text="用户注册",**btn_cfg,command=self.show_register).pack(pady=10)
        tk.Button(self.root, text="用户登录", **btn_cfg, command=self.show_login).pack(pady=10)
        tk.Button(self.root, text="添加餐厅", **btn_cfg, command=self.show_add_rest).pack(pady=10)
        tk.Button(self.root, text="查看所有餐厅", **btn_cfg, command=self.show_all_rest).pack(pady=10)
        tk.Button(self.root,text="搜索餐厅",**btn_cfg,command=self.show_search_rest).pack(pady=10)
        tk.Button(self.root, text="热门餐厅排行榜", **btn_cfg, command=self.show_hot_restaurants).pack(pady=10)
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

            success = register_user(
                username,
                pwd,
                taste,
                consume
            )
            if success:
                messagebox.showinfo("成功","注册成功！")
                self.show_main_menu()
            else:
                messagebox.showerror("错误","用户名已存在！")
            


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
            
            result=login_user(username,pwd)
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
        tk.Button(self.root, text="发表餐厅评价", **btn_cfg, command=self.show_add_comment).pack(pady=10)
        tk.Button(self.root,text="查看餐厅评价",**btn_cfg,command=self.show_comments).pack(pady=10)
        tk.Button(self.root, text="查看收藏餐厅", **btn_cfg, command=self.show_favorite).pack(pady=10)
        tk.Button(self.root, text="返回首页", **btn_cfg, command=self.show_main_menu).pack(pady=10)

    #5.智能推荐
    def show_recommend(self):
        self.clear_win()
        tk.Label(self.root,text="智能餐厅推荐",font=("黑体",18)).pack(pady=15)

        #表格组件
        cols=("餐厅名","菜系","人均价格","评分","地址","推荐分","推荐等级","推荐理由")
        tree=ttk.Treeview(self.root,columns=cols,show="headings",height=10)
        for c in cols:
            tree.heading(c,text=c)
        tree.column("餐厅名",width=120)
        tree.column("菜系",width=120)
        tree.column("人均价格",width=80)
        tree.column("评分",width=80)
        tree.column("地址",width=100)
        tree.column("推荐分",width=80)
        tree.column("推荐等级",width=90)
        tree.column("推荐理由",width=400)
        tree.pack(pady=10)

        res_list=show_recommend(self.current_user)
        if res_list:
            for r in res_list:
                tree.insert("","end",values=r)
        else:
            messagebox.showinfo("提示","暂无匹配的推荐餐厅！")

        def favorite():
            selected= tree.selection()
            if not selected:
                messagebox.showwarning("提示", "请先选择一个餐厅！")
                return
            item = tree.item(selected[0])
            rname = item["values"][0]
            success = add_favorite(self.current_user, rname)
            if success:
                messagebox.showinfo("成功", "收藏成功！")
            else:
                messagebox.showwarning("提示", "已经收藏过了！")
        tk.Button(self.root, text="收藏当前餐厅", font=("宋体", 12), command=favorite).pack(pady=10)
        tk.Button(self.root,text="返回",font=("宋体",12),command=self.show_user_func).pack(pady=10)

    #6.发表评论
    def show_add_comment(self):
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

        def submit_comment():
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
            
            success=show_add_comment(self.current_user,rname,u_score,content)
            if success:
                messagebox.showinfo("成功","评论提交成功！")
                self.show_user_func()
            else:
                messagebox.showerror("错误","餐厅不存在，评论提交失败！")
        tk.Button(self.root,text="提交评论",font=("宋体",12),command=submit_comment).pack(pady=20)
        tk.Button(self.root,text="返回",font=("宋体",12),command=self.show_user_func).pack(pady=20)

    #7.查看餐厅评价
    def show_comments(self):
        self.clear_win()
        tk.Label(self.root, text="查看餐厅评价", font=("黑体", 18)).pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack()

        tk.Label(frame, text="餐厅名称：", font=("宋体", 12)).grid(row=0, column=0, padx=10)
        ent_rname = tk.Entry(frame, width=30)
        ent_rname.grid(row=0, column=1)

        cols = ("用户名", "评分", "评价内容")
        tree = ttk.Treeview(self.root, columns=cols, show="headings", height=10)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=150)
        tree.pack(pady=15)

        def search_comments():
            rname = ent_rname.get().strip()
            if not rname:
                messagebox.showwarning("提示", "请输入餐厅名称！")
                return
            data = get_comments(rname)
            for item in tree.get_children():
                tree.delete(item)
            for item in data:
                tree.insert('', 'end', values=item)

        tk.Button(self.root, text="查询评价", command=search_comments).pack(pady=10)
        tk.Button(self.root, text="返回", command=self.show_user_func).pack()

    #8.添加餐厅
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
            success = add_restaurant(
                rname,
                ftype,
                price,
                score,
                addr
            )

            if success:
                messagebox.showinfo("成功", "餐厅添加成功！")
                self.show_main_menu()
            else:
                messagebox.showerror("错误", "餐厅已存在！")

        tk.Button(self.root,text="添加餐厅",font=("宋体",12),command=add_rest).pack(pady=20)
        tk.Button(self.root, text="返回首页", font=("宋体", 12), command=self.show_main_menu).pack()

    #9.查看全部餐厅
    def show_all_rest(self):
        self.clear_win()
        tk.Label(self.root,text="全部餐厅列表",font=("黑体",18)).pack(pady=15)

        cols=("餐厅名","菜系","人均价格","评分","地址")
        tree=ttk.Treeview(self.root,columns=cols,show="headings",height=10)
        for c in cols:
            tree.heading(c,text=c)
            tree.column(c,width=130)
        tree.pack(pady=10)

        data=get_all_restaurants()

        for item in data:
            tree.insert('','end',values=item)

        tk.Button(self.root,text="返回首页",font=("宋体",12),command=self.show_main_menu).pack(pady=10)

    #10.搜索餐厅
    def show_search_rest(self):
        self.clear_win()
        tk.Label(self.root,text="搜索餐厅",font=("黑体",18)).pack(pady=20)

        frame=tk.Frame(self.root)
        frame.pack()
        tk.Label(frame, text="请输入餐厅名称：", font=("宋体", 12)).grid(row=0, column=0, padx=10, pady=10)
        ent_keyword = tk.Entry(frame, width=30, font=("宋体", 12))
        ent_keyword.grid(row=0, column=1)

        cols=("餐厅名", "菜系", "人均价格", "评分", "地址")
        tree=ttk.Treeview(self.root,columns=cols,show="headings",height=10)
        for c in cols:
            tree.heading(c,text=c)
            tree.column(c,width=130)
        tree.pack(pady=10)

        def search():
            keyword = ent_keyword.get().strip()
            if not keyword:
                messagebox.showwarning("提示", "请输入餐厅名称！")
                return
            data = search_restaurant(keyword)
            for item in tree.get_children():
                tree.delete(item)
            if data:
                for item in data:
                    tree.insert('', 'end', values=item)
            else:
                messagebox.showinfo("提示", "未找到匹配的餐厅！")

        tk.Button(self.root, text="搜索", font=("宋体", 12), command=search).pack(pady=10)
        tk.Button(self.root, text="返回首页", font=("宋体", 12), command=self.show_main_menu).pack()
    #11.热门餐厅排行榜
    def show_hot_restaurants(self):
        self.clear_win()
        tk.Label(self.root, text="热门餐厅排行榜", font=("黑体", 18)).pack(pady=15)

        cols = ("排名","餐厅名", "菜系", "人均价格", "平均评分", "评论数")
        tree = ttk.Treeview(self.root, columns=cols, show="headings", height=10)
        for c in cols:
            tree.heading(c, text=c)
        tree.column("排名", width=60)
        tree.column("餐厅名", width=120)
        tree.column("菜系", width=120)
        tree.column("人均价格", width=90)
        tree.column("平均评分", width=90)
        tree.column("评论数", width=90)
        tree.pack(pady=10)
        data = get_hot_restaurants()
        print(data)
        rank = 1
        for item in data:
            tree.insert('', 'end', values=(rank, item[0], item[1], item[2], item[3], item[4]))
            rank += 1

        tk.Button(self.root, text="返回首页", font=("宋体", 12), command=self.show_main_menu).pack(pady=10)
    #12.查看收藏餐厅
    def show_favorite(self):
        self.clear_win()
        tk.Label(self.root, text="我的收藏餐厅", font=("黑体", 18)).pack(pady=15)

        cols = ("餐厅名", "菜系", "人均价格", "评分", "地址")
        tree = ttk.Treeview(self.root, columns=cols, show="headings", height=10)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120)
        tree.pack(pady=10)

        data = get_favorite(self.current_user)

        if data:
            for item in data:
                tree.insert('', 'end', values=item)
        else:
            messagebox.showinfo("提示", "您还没有收藏的餐厅！")

        tk.Button(self.root, text="返回", command=self.show_user_func).pack(pady=10)

if __name__ == "__main__":
    root=tk.Tk()
    app=RestaurantGUI(root)
    root.mainloop()
    























