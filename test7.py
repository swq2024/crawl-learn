import threading
import time

class MyThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        moyu_time(self.name, self.counter, 10, self.threadID)
        print("退出线程：" + self.name)

def moyu_time(threadName, delay, counter, threadID):
    while counter:
        time.sleep(delay)
        print("%s 开始摸鱼 %s 线程ID为: %s" % (threadName, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), threadID))
        counter -= 1
        if counter == 0:
            print("摸鱼结束")
            break
        else:
            continue

thread1 = MyThread(1, "Thread-1", 1) # 线程1延迟1秒 执行10次
thread2 = MyThread(2, "Thread-2", 2) # 线程2延迟2秒 执行10次

thread1.start()
thread2.start()

thread1.join()
thread2.join()
print("退出主线程")