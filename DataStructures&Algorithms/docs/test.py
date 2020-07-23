from datetime import datetime

scale = 10 ** 4
a = list(range(0,scale,-1))

all_times = []

test_number = 100

for i in range(test_number):
    start_time = datetime.now()
    1 in a
    end_time = datetime.now()
    time = end_time - start_time
    all_times.append(time)


for i in range(len(all_times)):
    if i == 0:
        sum = all_times[0]
    else:
        sum += all_times[i]

print("列表中有%d个元素，在索引100处插入一千个元素消耗的时间是：%s秒" % (scale, sum))