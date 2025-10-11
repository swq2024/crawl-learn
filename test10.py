from multiprocessing import Process
import multiprocessing

def foo(name):
    print('hello', name)
    print(multiprocessing.cpu_count()) # 打印电脑的cpu的内核数量

if __name__ == '__main__':
    p = Process(target=foo, args=('yuhuo',))
    p.start()
    p.join()