age = float(input('请输入你的年龄：'))
xl = float(input('请输入安静心率：'))
xb = ['男']
gender = input('请输入性别：')
if gender == xb[0]:
    n = 220
else:
    n = 210
xlmin = (n - age - xl) * 0.6 + xl
xlmax = (n - age - xl) * 0.8 + xl
print('您的最适宜运动心率为：', xlmin, '~', xlmax)
