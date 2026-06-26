from typing import List, Union, Any

An: List[Union[float, Any]] = []
an = float(input('请输入首项：'))
d = float(input('请输入公差：'))
n = int(input('请输入项数：'))
for i in range(n):
    An.append(an)
    an = an + d
print('数列为：', An)
sn = 0
for i in An:
    sn = sn + i
print('前 %d 项和为'%n, sn)
