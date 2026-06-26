#include <stdio.h>

int main() {
    int n;
    while (scanf("%d", &n) != EOF) {
        int found = 0;
        for (int i = 2992; i <= n; i++) {
            int dec = (i / 1000) + (i / 100 % 10) + (i / 10 % 10) + (i % 10);
            
            int tmp = i, duod = 0;
            while (tmp) {
                duod += tmp % 12;
                tmp /= 12;
            }
            tmp = i;
            int hex = 0;
            while (tmp) {
                hex += tmp % 16;
                tmp /= 16;
            }
            if (dec == duod && duod == hex) {
                printf("%d\n", i);
                found = 1;
            }
        }
        if (!found) puts("0");
    }
    return 0;
}