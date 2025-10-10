import time

def moyu_time(name, delay, counter):
    while counter:
        time.sleep(delay)
        print("%s 开始摸鱼 %s" % (name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        counter -= 1
        if counter == 0:
            print("摸鱼结束")
            break
        else:
            continue

if __name__ == '__main__':
    moyu_time('小明', 2, 5)


