from pymongo import MongoClient

conn = MongoClient('localhost', port=27017)

# 创建一个test数据库，如果不存在的话会自动创建
db = conn.test

"""
bust, waist, and hips 分别代表胸围、腰围和臀围
"""

# 插入一条数据
# db.col.insert_one({"name": '波多野結衣', 'bwh': { "b": 90, "w": 59, "h": 85} , 'age': 30})

# 批量插入数据
# db.col.insert_many([
#     {"name": '波多野結衣', 'bwh': { "b": 90, "w": 59, "h": 85} , 'age': 30},
#     {"name": '吉泽明步', 'bwh': { "b": 86, "w": 58, "h": 86} , 'age': 35},
#     {"name": '桃乃木香奈', 'bwh': { "b": 80, "w": 54, "h": 80} , 'age': 22},
#     {"name": '西宫梦', 'bwh': { "b": 85, "w": 56, "h": 86} , 'age': 22},
#     {"name": '松下纱荣子', 'bwh': { "b": 88, "w": 57, "h": 86} , 'age': 28}
# ])

# 查询所有数据
for item in db.col.find({}):
    print(item)

# 查询名字为吉泽明步的数据
# for item in db.col.find({"name": '吉泽明步'}):
#     print(item)

# 查询臀围小于等于85cm的数据
# for item in db.col.find({'bwh.h': {'$lte': 85}}):
#     print(item)

# 查询年龄大于25岁的数据
# for item in db.col.find({'age': {'$gt': 25}}):
#     print(item)

# 查询年龄大于25岁且胸围大于等于85cm的数据
# for item in db.col.find({'age': {'$gt': 25}, 'bwh.b': {'$gte': 85}}):
#     print(item)

# 删除名字为波多野結衣的数据
# db.col.delete_one({"name": "波多野結衣"})

# 批量删除年龄小于25岁的数据
# db.col.delete_many({'age': {'$lt': 25}})

# 删除所有数据
# db.col.delete_many({})

# 更新名字为波多野結衣的数据，将胸围改为83cm
# db.col.update_one({"name": "波多野結衣"}, {"$set": {"bwh.b": 83}})

# https://mp.weixin.qq.com/s?__biz=Mzg2NzYyNjg2Nw==&mid=2247489961&idx=1&sn=c04169582518b5f4d11f66aebb9c6b56&chksm=ceb9e3b5f9ce6aa30adbd449db4bb819fe55635f58dc93a5a5e316f2d246095a4d777df2ce55&cur_album_id=2448798954764255234&scene=189#wechat_redirect