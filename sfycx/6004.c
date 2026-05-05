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