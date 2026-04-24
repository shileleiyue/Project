Wb = 100000
n = 0
while Wb >= 0:
    Wb = round(Wb * (1+0.037), 2) - 20000
    n = n + 1
print(n, '年后资金全部取出')
