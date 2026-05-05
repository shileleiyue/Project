#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int start;
    int end;
} Interval;

int cmp(const void *a, const void *b) {
    Interval *ia = (Interval*)a;
    Interval *ib = (Interval*)b;
    return ia->start - ib->start;
}

int main() {
    int n;
    while (scanf("%d", &n) != EOF) {
        Interval *intervals = (Interval*)malloc(n * sizeof(Interval));
        for (int i = 0; i < n; i++) {
            int h1, m1, h2, m2;
            scanf("%d:%d %d:%d", &h1, &m1, &h2, &m2);
            intervals[i].start = h1 * 60 + m1;
            intervals[i].end   = h2 * 60 + m2;
        }
        qsort(intervals, n, sizeof(Interval), cmp);

        int total = 0;
        int cur_start = intervals[0].start;
        int cur_end   = intervals[0].end;
        for (int i = 1; i < n; i++) {
            if (intervals[i].start <= cur_end) {  
                if (intervals[i].end > cur_end)
                    cur_end = intervals[i].end;
            } else {
                total += cur_end - cur_start + 1;
                cur_start = intervals[i].start;
                cur_end   = intervals[i].end;
            }
        }
        total += cur_end - cur_start + 1;
        printf("%d\n", total);

        free(intervals);
    }
    return 0;
}