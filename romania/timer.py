"""
    计时器装饰器，打印函数运行n次所需要的时间。
    给函数加装饰器@timer后，调用函数时传参times = n，来调整函数运行的次数
    参数times的默认值为1，即加@timer装饰器的函数只执行一次。
"""
import time


def timer(func):
    def wrapper(*args, times = 1, name = "本函数", **kwargs):
        start = time.time()

        for i in range(times):
            result = func(*args, **kwargs)  

        end = time.time()
        time_used = end-start

        if time_used > 1:
            print("{}运行{}次使用了{}秒".format(name, times, round(time_used, 2)))
        elif time_used > 1 / 1000:
            print("{}运行{}次使用了{}毫秒".format(name, times, round(time_used * 1000, 2)))
        elif time_used > 1 / 1000**2:
            print("{}运行{}次使用了{}微秒".format(name, times, round(time_used * 1000 ** 2, 2)))
        elif time_used > 1 / 1000**3:
            print("{}运行{}次使用了{}纳秒".format(name, times, round(time_used * 1000 ** 3, 2)))

        return result

    return wrapper

if __name__ == "__main__":
    @timer
    def test():

        return 111


    hi = test(times = 100000000)
    print(hi)
