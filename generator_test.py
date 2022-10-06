# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/10/6
@Software: PyCharm
@disc:
======================================="""


def x(n):
    print("yield之前")
    yield n + 1
    print("yield之后")


def gen_test():
    x = 1
    while True:
        print(f"yield之前，x:[{x}]")
        y = yield x
        print(f"yield之后，x:[{x}], y:[{y}]")
        x *= 2
        print(f"yield之后后，x:[{x}], y:[{y}]")
        if y == -3:
            print(f"My heart is broken")
            break


if __name__ == '__main__':
    a = x(10)
    print(next(a))
    print(next(a))
    gt = gen_test()
    print(next(gt))
    print(next(gt))
    print(next(gt))
    print(next(gt))
    print(next(gt))
    print(next(gt))
    print(next(gt))
    print(next(gt))
    print(next(gt))
