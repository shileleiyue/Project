#include <stdio.h>

int main() {
    int n;
    for(scanf("%d", &n); n != 0; scanf("%d", &n)) {
        int dec = (n / 1000) + (n / 100 % 10) + (n / 10 % 10) + (n % 10);
        int tmp = n, duod = 0;
        while (tmp) {
            duod += tmp % 12;
            tmp /= 12;
        }
        tmp = n;
        int hex = 0;
        while (tmp) {
            hex += tmp % 16;
            tmp /= 16;
        }
        if (dec == duod && duod == hex) {
            printf("%d is a Sky Number.\n", n);
        }
        else {
            printf("%d is not a Sky Number.\n", n);
        }
    }
    return 0;
}