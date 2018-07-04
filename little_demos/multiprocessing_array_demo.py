from multiprocessing import Process, Value, Array
import itertools

def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]
    a[1:4] = b'\0'*3
    

if __name__ == '__main__':
    num = Value('d', 0.0)
    arr = Array('i', range(10))

    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])
    print(dir(arr))  # ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getslice__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__setslice__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_lock', '_obj', 'acquire', 'get_lock', 'get_obj', 'release']
    # arr[1:4] = [i for i in itertools.repeat(0,3)]
    # arr[1:4] = b'\0'*3
    # print(arr[:])

    # 以下都不行。 ValueError: Can only assign sequence of same size
    # arr[:] = 0
    # arr[1:3] = [0, 0, 0]
    # arr[1:4] = itertools.repeat(0,3)