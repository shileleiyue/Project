#include <stdio.h>
#include <math.h>

int main() {
    int n;
    int firstCase = 1;   // 标记是否为第一个输入，用于控制空行
    while (scanf("%d", &n) != EOF) {
        int count = 0;
        // 枚举 x，因为 x <= y，所以 x*x <= n/2
        int limit = (int)sqrt(n / 2.0);
        for (int x = 1; x <= limit; ++x) {
            int remain = n - x * x;
            int y = (int)sqrt(remain);
            if (y * y == remain && y >= x) {  // 检查 y 是否为整数且不小于 x
                ++count;
                if (count == 1 && !firstCase) {
                    printf("\n");   // 两个不同的 n 之间输出空行
                }
                firstCase = 0;
                printf("No %d: %d * %d + %d * %d = %d\n", count, x, x, y, y, n);
            }
        }
    }
    return 0;
}