#算法区
suanfa = {'加法': '求和', '减法': '求差', '乘法': '求积', '除法': '求商', '幂': '底数和指数', '阶和': '阶和次数', '阶乘': '阶乘次数', '数列': '首项和公差', '计数': '元素个数和所需取出元素个数'}
xy = ['加法', '减法', '乘法', '除法', '幂', '阶和', '阶乘',  '数列', '计数']
print('本计算器所能支持的算法有：', xy)
a, b = 1, 1
def jsgc():
    sf = input('请输入您想使用的算法：')
    if sf == xy[0] or xy[1] or xy[2] or xy[3] or xy[4] or xy[5] or xy[6] or xy[7] or xy[8]:
        print('请输入', suanfa[sf], '的值：')
        a, b = float(input('')), float(input(''))
    elif sf == xy[5] or sf[6]:
        print('请输入', suanfa[sf], '的值：')
        c = float(input(''))

#函数定义区
def addittion():
    d = a + b
    print(a, '+', b, '=', d)


def subtraction():
    d = a - b
    print(a, '-', b, '=', d)


def multiplication():
    d = a * b
    print(a, '*', b, '=', d)


def division():
    d = a / b
    print(a, '/', b, '=', d)


def power_function():
    d = a ** b
    print(a, '**', b, '=', d)


def step_sum():
    b, m = 0, 1
    while m <= c:
        b = m + b
        m = m + 1
    print('阶和', c, '次的阶和值为', b)


def factorial():
    b, m = 1, 1
    while m <= c:
        b = m * b
        m = m + 1
        print('阶乘', c, '次的阶乘值为', b)


def series():
    n = 1
    while n <= n:
        Na = a + (n - 1) * b
        n = n + 1
        print(Na)


def tally():
    jishu = ['排列', '组合']
    jsff = input('排列还是组合:')
    d = a - b
    n1, n2, n3, jg1, jg2, jg3 = 1, 1, 1, 1, 1, 1
    while n1 <= a:
        jg1 = n1 * jg1
        n1 = n1 + 1
    while n2 <= b:
        jg2 = n2 * jg2
        n2 = n2 + 1
    while n3 <= d:
        jg3 = n3 * jg3
        n3 = n3 + 1
    if jsff == jishu[0]:
        jg4 = jg1 / jg3
        print('从', a, '个元素中选出', b, '个元素进行排列，共有', jg4, '种选法。')
    if jsff == jishu[1]:
        jg5 = jg1 / (jg2 * jg3)
        print('从', a, '个元素中选出', b, '个元素进行组合，共有', jg5, '种选法')


    # 执行区
if sf == xy[0]:
    addittion()
elif sf == xy[1]:
    subtraction()
elif sf == xy[2]:
    multiplication()
elif sf == xy[3]:
    division()
elif sf == xy[4]:
    power_function()
elif sf == xy[5]:
    step_sum()
elif sf == xy[6]:
    factorial()
elif sf == xy[7]:
    series()
elif sf == xy[8]:
    tally()
else:
    print('本计算器还不具备该算法！')
def gg():
    gg = float(input(''))
    if gg == 1:
        return (jsgc())
jsgc()