// 题目描述
// 僵尸最爱吃脑袋了。
// 输入
// 第一行包含了一个整数n表示测试数据的组数。
// 接下来的n行，每一行由（X，Y）构成，X表示僵尸要吃掉的大脑数目，Y表示僵尸存活下来所需要的大脑数目。
// 输出
// 对于每组测试数据，输出一行，如果僵尸要吃掉的大脑数目大于或等于所需要的大脑数目，要输出“MMM BRAINS”，否则，输出“NO BRAINS”。
// 样例输入 复制
// 3
// 4 5
// 3 3
// 4 3 
// 样例输出 复制
// NO BRAINS
// MMM BRAINS
// MMM BRAINS

#include <stdio.h>

int main() {
    int n, x, y;
    scanf("%d", &n);
    while (n--) {
        scanf("%d %d", &x, &y);
        if (x >= y)
            printf("MMM BRAINS\n");
        else
            printf("NO BRAINS\n");
    }
    return 0;
}