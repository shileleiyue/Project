// 题目描述
// Gardon的18岁生日就要到了，他当然很开心，可是他突然想到一个问题，是不是每个人从出生开始，到达18岁生日时所经过的天数都是一样的呢？似乎并不全都是这样，所以他想请你帮忙计算一下他和他的几个朋友从出生到达18岁生日所经过的总天数，让他好来比较一下。
// 输入
// 一个整数T，表示测试数据的组数,接下来有T行日期,每行一个，格式是YYYY-MM-DD。如我的生日是1988-03-07。
// 输出
// T行，每行一个数，表示此人从出生到18岁生日所经过的天数。如果这个人没有18岁生日，就输出-1。
// 样例输入 复制
// 1
// 1988-03-07
// 样例输出 复制
// 6574

#include <stdio.h>

int is_leap(int year) {
    return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
}
int days_since_epoch(int year, int month, int day) {
    int days = 0;
    for (int y = 1; y < year; y++) {
        days += is_leap(y) ? 366 : 365;
    }
    int month_days[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    if (is_leap(year)) month_days[1] = 29;
    for (int m = 0; m < month - 1; m++) {
        days += month_days[m];
    }
    days += day;
    return days;
}

int main() {
    int T;
    scanf("%d", &T);
    while (T--) {
        int y, m, d;
        scanf("%d-%d-%d", &y, &m, &d);
        if (m == 2 && d == 29 && !is_leap(y + 18)) {
            printf("-1\n");
        } else {
            int birth = days_since_epoch(y, m, d);
            int adult = days_since_epoch(y + 18, m, d);
            printf("%d\n", adult - birth);
        }
    }
    return 0;
}