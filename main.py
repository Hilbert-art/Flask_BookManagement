import flask
from flask import *
import pymysql
import hashlib
import json

# 创建Flask程序并定义模板位置
app = Flask(__name__,
            static_url_path='/static',
            static_folder='static',
            template_folder='templates'
            )


# 将所有对主页面的访问都跳转到登录框
@app.route('/', methods=['GET', 'POST'])
def index():
    return flask.redirect(flask.url_for('log_in'))


# 处理普通用户登陆
@app.route('/log_handle', methods=['POST'])
def log_handle():
    find_user = False
    if request.method == 'POST':
        # username和password是前端log_in.html的name字段里的字符
        username = request.form.get('username')
        password = request.form.get('password')
        # 对密码进行md5处理
        encrypass = hashlib.md5()
        encrypass.update(password.encode(encoding='utf-8'))
        password = encrypass.hexdigest()

    # 通过mysql进行存储
    db = pymysql.connect(host="localhost", user="root", password="root", db="www")

    # 创建数据库指针cursor
    cursor = db.cursor()

    sql = "SELECT * FROM users"

    # 执行数据库命令并将数据提取到cursor中
    cursor.execute(sql)
    # 确认命令
    db.commit()
    user_list = []
    for item in cursor.fetchall():
        dict_user = {'username': item[0], 'password': item[1]}
        user_list.append(dict_user)
    # 对数据库中所有的数据进行遍历,找出username
    for i in range(len(user_list)):
        if user_list[i]['username'] == username:
            if user_list[i]['password'] == password:
                find_user = True
                break
            else:
                break

    db.close()
    if not find_user:
        # 登录失败就跳转倒log_fail中并弹窗
        return flask.render_template("log_fail.html")

    else:
        # 登录成功就跳转log_success(用户界面)
        return flask.redirect(flask.url_for('log_success'))


# 处理admin用户的登陆
@app.route("/log_handle_admin", methods=['POST'])
def log_handle_admin():
    find_user = False
    if request.method == 'POST':
        # username和password是前端log_in.html的name字段里的字符
        username = request.form.get('username')
        password = request.form.get('password')
        # 对密码进行md5处理
        encrypass = hashlib.md5()
        encrypass.update(password.encode(encoding='utf-8'))
        password = encrypass.hexdigest()

    # 通过mysql进行存储
    db = pymysql.connect(host="localhost", user="root", password="root", db="www")

    # 创建数据库指针cursor
    cursor = db.cursor()

    sql = "SELECT * FROM administrator"

    # 执行数据库命令并将数据提取到cursor中
    cursor.execute(sql)
    # 确认命令
    db.commit()
    user_list = []
    for item in cursor.fetchall():
        dict_user = {'username': item[0], 'password': item[1]}
        user_list.append(dict_user)
    # 对数据库中所有的数据进行遍历,找出username
    for i in range(len(user_list)):
        if user_list[i]['username'] == username:
            if user_list[i]['password'] == password:
                find_user = True
                break
            else:
                break

    db.close()
    if not find_user:
        # 登录失败就跳转倒log_fail中并弹窗
        return flask.render_template("log_fail_admin.html")

    else:
        # 登录成功就跳转log_success(管理员界面)
        return flask.redirect(flask.url_for('log_success_admin'))


# 处理注册
@app.route('/register_handle', methods=['POST'])
def register_handle():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        # 判断两次密码是否正确
        if password == confirm_password:
            # 对密码进行md5处理
            encrypass = hashlib.md5()
            encrypass.update(password.encode(encoding='utf-8'))
            password = encrypass.hexdigest()

            db = pymysql.connect(host="localhost", user="root", password="root", db="www")
            cursor = db.cursor()

            search_sql = "SELECT * FROM users"
            cursor.execute(search_sql)
            db.commit()
            if cursor.fetchall() is None:
                user_list = []
                for item in cursor.fetchall():
                    dict_user = {'username': item[0], 'password': item[1]}
                    user_list.append(dict_user)
                for i in range(len(user_list)):
                    # 判断是否存在相同用户名
                    if user_list[i]['username'] != username:
                        # 将用户名和加密后的密码插入数据库
                        sql = "INSERT INTO users VALUES('%s','%s')" % (username, password)
                        cursor.execute(sql)
                        db.commit()
                    else:
                        have_same_username = 1
                        return flask.render_template("register_fail.html", have_same_username=have_same_username)
            else:
                sql = "INSERT INTO users VALUES('%s','%s')" % (username, password)
                cursor.execute(sql)
                db.commit()
        else:
            two_passwd_wrong = 1
            return flask.render_template("register_fail.html", two_passwd_wrong=two_passwd_wrong)
    db.close()
    return flask.redirect(flask.url_for('log_in'))


@app.route('/log_in', methods=['GET'])
def log_in():
    return render_template('log_in.html')


@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/log_success')
def log_success():
    db = pymysql.connect(host="localhost", user="root", password="root", db="book_manager")
    cursor = db.cursor()
    sql = "SELECT * FROM books"
    cursor.execute(sql)
    db.commit()
    data = cursor.fetchall()
    db.close()
    return render_template('log_success.html', show_list=data)


@app.route('/log_success_admin')
def log_success_admin():
    db = pymysql.connect(host="localhost", user="root", password="root", db="book_manager")
    cursor = db.cursor()
    sql = "SELECT * FROM books"
    cursor.execute(sql)
    db.commit()
    data = cursor.fetchall()
    db.close()
    return render_template('log_success_admin.html', show_list=data)


@app.route('/log_in_admin')
def log_in_admin():
    return render_template('log_in_admin.html')


# 获取ajax前端POST请求
@app.route('/books/add', methods=['POST'])
def books_add():
    params_list = []
    btitle = request.form.get('btitle')
    bauthor = request.form.get('bauthor')
    bperson = request.form.get('bperson')
    bpub_date = request.form.get('bpub_date')
    bread = request.form.get('bread')
    params_list.append(btitle)
    params_list.append(bauthor)
    params_list.append(bperson)
    params_list.append(bpub_date)
    params_list.append(bread)

    # 创建Connection连接
    conn = pymysql.connect(host='localhost', port=3306, db='book_manager', user='root', password='root',
                           charset='utf8')
    # 获得Cursor对象
    cs1 = conn.cursor()

    cs1.execute("insert into books(btitle,bauthor,bperson,bpub_date,bread) values(%s,%s,%s,%s,%s)",
                params_list)
    # 得到数据库的数据
    conn.commit()

    # 关闭
    conn.close()
    # 返回json数据
    return Response('{"data": "增加成功！"}')


@app.route("/books/delete", methods=['POST'])
def books_delete():
    # 接收ajax发送的post请求的数据
    body_data = request.get_data()
    # 解析json成字典
    params_dict = json.loads(body_data)

    # 创建Connection连接
    conn = pymysql.connect(host='localhost', port=3306, db='book_manager', user='root', password='root',
                           charset='utf8')
    # 获得Cursor对象
    cs1 = conn.cursor()

    # 执行查询的sql语句
    cs1.execute("delete from books where id = %(id)s", params_dict)

    conn.commit()

    # 关闭
    conn.close()
    # 返回json数据
    return Response('{"data": "删除成功！"}')


@app.route("/books/update", methods=['POST'])
def books_update():
    # 接收ajax发送的post请求的数据
    body_data = request.get_data()
    # 解析json成字典
    params_dict = json.loads(body_data)

    # 创建Connection连接
    conn = pymysql.connect(host='localhost', port=3306, db='book_manager', user='root', password='root',
                           charset='utf8')
    # 获得Cursor对象
    cs1 = conn.cursor()

    cs1.execute(
        "update books set btitle = %(btitle)s,bauthor = %(bauthor)s,bperson = %(bperson)s,bpub_date =%("
        "bpub_date)s,bread = %(bread)s where id = %(id)s",
        params_dict
    )

    conn.commit()

    # 断开连接
    conn.close()

    # 返回json数据
    return Response('{"data": "更新成功！"}')


# 自定义404页面
@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template("404.html"), 404


if __name__ == '__main__':
    # 调试时需要debug=True
    app.run()
