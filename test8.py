from concurrent.futures import ThreadPoolExecutor
import time

def moyu_time(name, delay, counter):
    while counter:
        time.sleep(delay)
        print("%s 开始摸鱼 %s" % (name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        counter -= 1
        if counter == 0:
            print("%s 摸鱼结束" % name)
            break
        else:
            continue

if __name__ == '__main__':
    pool = ThreadPoolExecutor(20)
    for i in range(1, 5):
        pool.submit(moyu_time("小明" + str(i), 1, 3))
