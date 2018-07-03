from multiprocessing import Process, Queue
import json
import time
import os
# from queue import Queue


# 写数据进程执行的代码:
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)


def output_writer(q: Queue):
    path = 'output/test.json'
    # 重新启动程序后先清空
    with open(path, 'wb') as f:
        f.write(b'[]')

    while True:
        if not q.empty():
            data = json.load(open(path, 'rb'))
            while not q.empty():
                it = q.get()
                data.append(it)
            # print('data:', data)
            json.dump(data, open(path, 'wt'), indent=2)
            # open(path, 'wb').write(json.dumps(data))
        time.sleep(2)


if __name__ == '__main__':
    output_queue = Queue()
    Process(target=read, args=(output_queue,)).start()
    while True:
        inp = input('>>>')
        if inp == '':
            break
        print(inp)
        output_queue.put(inp)

