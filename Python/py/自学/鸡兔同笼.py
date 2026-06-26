a = int(input('请输入总的头数：'))
b = int(input('请输入总的足数：'))
t = int((b - 2 * a)/2)
j = int(a - t)
if t >= 0:
    if j >= 0:
        print('兔子的数量为', t, '鸡的数量为', j)
if t < 0 and j < 0:
    print('无解')

