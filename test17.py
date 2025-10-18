import pymysql
import pandas as pd
from sqlalchemy import create_engine

db = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    # database='Movies', # 指定连接到 Movies 数据库 如果不存在该数据库则不可指定, 需要先创建数据库
    cursorclass=pymysql.cursors.DictCursor  # cursor会以字典的形式返回结果集
)

cursor = db.cursor()

# 创建 DoubanMovies 数据库并把字符集设置为 UTF-8 ，防止中文乱码
sql0 = """
    CREATE DATABASE IF NOT EXISTS Movies CHARACTER SET utf8 COLLATE utf8_general_ci;
"""

try:
    cursor.execute(sql0)
    print('Success: 创建 Movies 数据库成功')
    db.select_db('Movies')
    print('Success: 切换到 Movies 数据库成功')
except Exception as e:
    print('Error: 创建 Movies 数据库失败', e)


# 创建 doubanmovies 表
sql1 = """
    CREATE TABLE IF NOT EXISTS doubanmovies (
        id INT PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(255),
        img VARCHAR(255),
        rating FLOAT,
        quote TEXT
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
# 先删除可能存在的旧表(如果存在)
cursor.execute("DROP TABLE IF EXISTS doubanmovies")
# 然后创建新表
cursor.execute(sql1)
db.commit()  # 确保表创建提交

df = pd.read_csv('douban_top250_movies1.csv')
# print(df)

# 使用相同的连接引擎插入数据
engine = create_engine('mysql+pymysql://root:123456@localhost/Movies?charset=utf8')
with engine.connect() as conn, conn.begin():
    # 先检查表是否存在 注意: MySQL在Windows系统下默认是大小写敏感的，所以下面指定表名需要与数据库中的表名称完全一致
    if engine.dialect.has_table(conn, 'doubanmovies'):
        # 使用该方法会丢失 id 列 index=False 表示不使用索引
        rows = df.to_sql('doubanmovies', con=conn, if_exists='replace', index=False)
        if rows > 0:
            print(f"Success: Inserted {rows} rows into doubanmovies table.")
            print('Success: 插入数据成功')
        else:
            print("Error: No rows inserted into doubanmovies table.")
    else:
        print("Error: doubanmovies table does not exist")

sql2 = """
    SELECT * FROM doubanmovies LIMIT 10;
"""
cursor.execute(sql2) # 只查询10条数据
print(cursor.fetchmany(size=5)) # 打印前5条数据

db.close()