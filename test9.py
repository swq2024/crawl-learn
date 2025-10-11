import threading
import time
from queue import Queue

class CustomThread(threading.Thread):
    def __init__(self, queue):
        # 调用父类threading.Thread的构造函数
        threading.Thread.__init__(self)
        # 将传入的queue赋值给类的私有属性__queue
        self.__queue = queue
    def run(self):
        # 进入一个无限循环
        while True:
            # 从队列中获取一个方法
            q_method = self.__queue.get()
            # 执行获取到的方法
            q_method()
            # 标记任务完成
            self.__queue.task_done()

def moyu():
    print("开始摸鱼 %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


def queue_pool():
    # 创建一个最大容量为5的队列
    queue = Queue(5)
    print("queue.maxsize", queue.maxsize)

    # 启动多个线程，每个线程的最大数量为队列的最大容量
    for i in range(queue.maxsize):
        # 创建自定义线程对象，并将队列作为参数传入
        t = CustomThread(queue)
        # 设置线程为守护线程
        t.daemon = True
        # 启动线程
        t.start()

    # 向队列中添加20个元素
    for i in range(20):
        # 向队列中添加一个方法
        queue.put(moyu)

    # 等待队列中的所有任务完成
    queue.join()

if __name__ == '__main__':
    queue_pool()
