#include <stdio.h>
#include <string.h>

int main() {
    char *haab_months[] = {
        "pop", "no", "zip", "zotz", "tzec", "xul", "yoxkin", "mol", "chen",
        "yax", "zac", "ceh", "mac", "kankin", "muan", "pax", "koyab", "cumhu",
        "uayet"
    };
    char *tzolkin_days[] = {
        "imix", "ik", "akbal", "kan", "chicchan", "cimi", "manik", "lamat",
        "muluk", "ok", "chuen", "eb", "ben", "ix", "mem", "cib", "caban",
        "eznab", "canac", "ahau"
    };

    int n;
    scanf("%d", &n);
    printf("%d\n", n);

    for (int i = 0; i < n; i++) {
        int day, year;
        char month[10];
        scanf("%d. %s %d", &day, month, &year);
        int month_idx;
        for (month_idx = 0; month_idx < 19; month_idx++) {
            if (strcmp(month, haab_months[month_idx]) == 0)
                break;
        }

        int total_days = year * 365 + month_idx * 20 + day;

        int tzolkin_year = total_days / 260;
        int number = total_days % 13 + 1;
        int name_idx = total_days % 20;

        printf("%d %s %d\n", number, tzolkin_days[name_idx], tzolkin_year);
    }
    return 0;
}