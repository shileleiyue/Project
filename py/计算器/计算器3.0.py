def jsq_jhb():
    xy = ['加法', '减法', '乘法', '除法', '幂', '阶乘', '阶和', '数列', '计数', '开方']
    print('本计算器所能支持的算法有：', xy)
    sf = input('请输入您想使用的算法：')
    if sf == xy[0]:
        print()
        a, b = float(input('')), float(input(''))
        c = a + b
        print(a, '+', b, '=', c)
    elif sf == xy[1]:
        print('请输入被减数和减数：')
        a, b = float(input('')), float(input(''))
        c = a - b
        print(a, '-', b, '=', c)
    elif sf == xy[2]:
        print('请输入两个因数：')
        a, b = float(input('')), float(input(''))
        c = a * b
        print(a, '×', b, '=', c)
    elif sf == xy[3]:
        print('请输入被除数和除数：')
        a, b = float(input('')), float(input(''))
        c = a / b
        print(a, '÷', b, '=', c)
    elif sf == xy[4]:
        print('请输入底数和指数：')
        a, b = float(input('')), float(input(''))
        c = a ** b
        print(a, '**', b, '=', c)
    elif sf == xy[5]:
        print('请输入阶乘次数：')
        a = float(input(''))
        b = 1
        m = 1
        while m <= a:
            b = m * b
            m = m + 1
            print('阶乘', a, '次的阶乘值为', b)
    elif sf == xy[6]:
        print('请输入阶和次数：')
        a = float(input(''))
        b = 0
        m = 1
        while m <= a:
            b = m + b
            m = m + 1
        print('阶和', a, '次的阶和值为', b)
    elif sf == xy[7]:
        print('请输入a1和d的值：')
        a1, d = float(input('')), float(input(''))
        print('请输入所需项数：')
        n0 = float(input(''))
        n = 1
        while n <= n0:
            Na = a1 + (n - 1) * d
            n = n + 1
            print(Na)
    elif sf == xy[8]:
        jishu = ['排列', '组合']
        print('请输入元素个数和所需选出元素个数:')
        a, b = float(input('')), float(input(''))
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
            n3 = n3 +1
        if jsff == jishu[0]:
            jg4 = jg1 / jg3
            print('从', a, '个元素中选出', b, '个元素进行排列，共有', jg4, '种选法。')
        if jsff == jishu[1]:
            jg5 = jg1 / (jg2 * jg3)
            print('从', a, '个元素中选出', b, '个元素进行组合，共有', jg5, '种选法。')
    elif sf == xy[9]:
        num = float(input("需要开方的数："))
        num1 = num ** 0.5
        print(num, '的开方数为：', num1)
    else:
        print('本计算器还不具备该算法！')

jsq_jhb()
