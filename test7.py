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
        moyu_time(self.name, self.counter, 10)
        print("退出线程：" + self.name)

def moyu_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print("%s 开始摸鱼 %s" % (threadName, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
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

# https://mp.weixin.qq.com/s?__biz=Mzg2NzYyNjg2Nw==&mid=2247489908&idx=1&sn=19c8dfda7163f221a8490cd0a64966e4&chksm=ceb9e368f9ce6a7e223fabb30afc70cac4f30eff3acca0656e3df0fdbb1dbc2d4a300b0c2d2e&cur_album_id=2448798954764255234&scene=189#wechat_redirect