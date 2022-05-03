# Flask_BookManagement
### 简介

Flask+Mysql，基于之前写过的flask的登录框，添加图书管理系统的功能，并基于ajax实现无刷页面

### 功能

1.一个登录框，具备创建用户，并判断是否存在或者用户重名并插入数据库

2.登录后跳转用户查询界面并正常登出

3.利用flask的路由绑定，避免显示文件后缀，同时对没有路由的页面做404处理

4.有管理员专门的登录窗口，进去后进入管理员界面

5.管理员界面拥有查询图书、删除图书、修改图书、增加图书的功能

### 使用配置

1.通过phpstudy建立mysql数据库，我使用的是5.7.26版本，用户名和密码都是root

2.创建用户、管理员、图书表，并插入数据

3.开放5000端口

### 数据库预配置

```python
# 创建用户/管理员数据库
create database www;
use www;
create table user (username varchar(100) not null,password varchar(100) not null);
create table administrator (username varchar(100) not null,password varchar(100) not null);

# 预设管理员账密，admin/admin，密码md5加密
insert into administrator values('admin','21232f297a57a5a743894a0e4a801fc3');

# 创建图书数据库
create database book_manager charset=utf8;
use book_manager;
CREATE TABLE books(id int UNSIGNED PRIMARY KEY AUTO_INCREMENT ,btitle VARCHAR(30) not NULL ,bauthor VARCHAR(30) NOT NULL ,bperson VARCHAR(30),bpub_date DATE NOT NULL ,bread INT UNSIGNED);

# 插入图书数据
insert into books(btitle, bauthor, bperson, bpub_date, bread) VALUES
('红楼梦','曹雪芹','宝玉','1980-5-1',12),
('西游记','施耐安','悟空','1986-7-24',36),
('水浒传','吴承恩','林冲','1995-12-24',20),
('三国演义','罗贯中','曹操','1980-5-1',58);
```

