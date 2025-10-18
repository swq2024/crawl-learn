import pymysql

db = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='Test', # 指定连接到 Test 数据库 如果不存在该数据库则不可指定, 需要先创建数据库
    cursorclass=pymysql.cursors.DictCursor  # cursor会以字典的形式返回结果集
)

# print(db) # <pymysql.connections.Connection object at 0x000001CE6B1E92B0>

# 产生 cursor 对象, 用于执行 SQL 语句
cursor = db.cursor()

# 创建 Test 数据库
sql0 = """
    CREATE DATABASE IF NOT EXISTS Test;
"""
cursor.execute(sql0)
db.select_db('Test') # 切换到 Test 数据库 相当于执行 use Test

# 创建 TestData 表
# sql1 = """CREATE TABLE TestData (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     name VARCHAR(20) NOT NULL,
#     age INT
# )"""
# cursor.execute(sql1)

# 插入数据
# sql2 = """
#     INSERT INTO TestData (name, age) VALUES ("张三", 18)
# """
# try:
#     rows = cursor.execute(sql2)
#     db.commit() # 当执行插入，更新，删除数据时需要提交事务
#     if rows > 0:
#         print("插入数据成功")
# except Exception as e:
#     print("插入数据失败")
#     db.rollback()

# 查询数据
sql3 = """
    SELECT * FROM TestData
"""
cursor.execute(sql3)
print(cursor.fetchall()) # 打印查询到的所有数据

# 修改数据
# sql4 = """
#     UPDATE TestData SET age = 20 WHERE name = "张三"
# """

# try:
#     rows = cursor.execute(sql4)
#     db.commit()
#     if rows > 0:
#         print("修改数据成功")
# except Exception as e:
#     print("修改数据失败")
#     db.rollback()

# 删除数据
# sql5 = """DELETE FROM TestData WHERE name = '%s' and age = '%d'""" % ('张三', 20) 

# try:
#     rows = cursor.execute(sql5)
#     db.commit()
#     if rows > 0:
#         print("删除数据成功")
#     else:
#         print("没有找到要删除的数据")
# except Exception as e:
#     print("删除数据失败")
#     db.rollback()

db.close()
