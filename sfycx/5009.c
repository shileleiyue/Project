// 题目描述
// 将M进制的数X转换为N进制的数输出。

// 输入
// 输入有多组测试数据。

// 输入的第一行包括两个整数：M和N(2<=M,N<=36)。
// 下面的一行输入一个数X，X是M进制的数，现在要求你将M进制的数X转换成N进制的数输出。

// 输出
// 输出X的N进制表示的数。

// 样例输入 复制
// 10 2
// 11
// 样例输出 复制
// 1011
// 提示
// 注意输入时如有字母，则字母为大写，输出时如有字母，则字母为小写。

#include <stdio.h>
#include <string.h>

int main() {
    int m, n;
    char x[256];  // 存放 M 进制数的字符串

    // 多组测试数据，直到文件结束
    while (scanf("%d %d", &m, &n) == 2) {
        scanf("%s", x);  // 读入 M 进制数

        // 第一步：将 M 进制字符串转换成十进制整数（用 long long 防溢出）
        long long decimal = 0;
        for (int i = 0; x[i] != '\0'; i++) {
            int digit;
            if (x[i] >= '0' && x[i] <= '9')
                digit = x[i] - '0';          // 数字 0-9
            else if (x[i] >= 'A' && x[i] <= 'Z')
                digit = x[i] - 'A' + 10;     // 字母 A-Z 表示 10-35
            else
                continue;                    // 忽略非法字符（题目保证不会出现）
            decimal = decimal * m + digit;
        }

        // 第二步：将十进制整数转换成 N 进制，结果逆序存入数组
        char result[256];
        int idx = 0;

        if (decimal == 0) {
            result[idx++] = '0';   // 单独处理 0 的情况
        } else {
            while (decimal > 0) {
                int remainder = decimal % n;
                decimal /= n;
                if (remainder < 10)
                    result[idx++] = remainder + '0';
                else
                    result[idx++] = (remainder - 10) + 'a';  // 小写字母
            }
        }

        // 第三步：从后往前输出，即为目标进制数
        for (int i = idx - 1; i >= 0; i--)
            putchar(result[i]);
        putchar('\n');   // 每个结果占一行
    }

    return 0;
}